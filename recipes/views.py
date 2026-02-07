import random
from datetime import date, timedelta

from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView

from .forms import RecipeForm
from .models import Recipe, Tag

from rest_framework import generics, filters
from .serializers import RecipeSerializer


class RecipeListView(ListView):
    model = Recipe
    template_name = "recipes/recipe_list.html"
    context_object_name = "recipes"
    paginate_by = 12

    def get_queryset(self):
        qs = Recipe.objects.prefetch_related("tags").all()

        q = self.request.GET.get("q", "").strip()
        mood = self.request.GET.get("mood", "").strip()
        tag = self.request.GET.get("tag", "").strip()
        fav = self.request.GET.get("fav", "").strip()

        if q:
            qs = qs.filter(
                Q(title__icontains=q) |
                Q(description__icontains=q) |
                Q(ingredients__icontains=q)
            )
        if mood:
            qs = qs.filter(mood=mood)
        if tag:
            qs = qs.filter(tags__name=tag.lower())
        if fav == "1":
            qs = qs.filter(is_favorite=True)

        return qs.distinct()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["moods"] = Recipe.MOOD_CHOICES
        ctx["tags"] = Tag.objects.all()
        ctx["filters"] = {
            "q": self.request.GET.get("q", ""),
            "mood": self.request.GET.get("mood", ""),
            "tag": self.request.GET.get("tag", ""),
            "fav": self.request.GET.get("fav", ""),
        }
        return ctx


class RecipeDetailView(DetailView):
    model = Recipe
    template_name = "recipes/recipe_detail.html"
    context_object_name = "recipe"


class RecipeCreateView(CreateView):
    model = Recipe
    form_class = RecipeForm
    template_name = "recipes/recipe_form.html"


class RecipeUpdateView(UpdateView):
    model = Recipe
    form_class = RecipeForm
    template_name = "recipes/recipe_form.html"


class RecipeDeleteView(DeleteView):
    model = Recipe
    template_name = "recipes/recipe_confirm_delete.html"

    def get_success_url(self):
        return reverse("recipes:list")


def toggle_favorite(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    recipe.is_favorite = not recipe.is_favorite
    recipe.save(update_fields=["is_favorite"])
    return HttpResponseRedirect(request.META.get("HTTP_REFERER", reverse("recipes:detail", args=[pk])))


class TodaysPickView(TemplateView):
    template_name = "recipes/todays_pick.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        mood = self.request.GET.get("mood", "").strip()

        qs = Recipe.objects.prefetch_related("tags").all()
        if mood:
            qs = qs.filter(mood=mood)

        recipes = list(qs)
        ctx["moods"] = Recipe.MOOD_CHOICES
        ctx["selected_mood"] = mood
        ctx["pick"] = random.choice(recipes) if recipes else None
        return ctx


class WeeklyMealPlanPrintView(TemplateView):
    """
    Super simple: picks 7 recipes (random) and shows a print-friendly page.
    Later you can make it user-selected.
    """
    template_name = "recipes/meal_plan_print.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        all_recipes = list(Recipe.objects.all())
        plan = []

        start = date.today()
        for i in range(7):
            day = start + timedelta(days=i)
            pick = random.choice(all_recipes) if all_recipes else None
            plan.append((day, pick))

        ctx["plan"] = plan
        return ctx



class RecipeListAPI(generics.ListCreateAPIView):
    queryset = Recipe.objects.prefetch_related("tags").all()
    serializer_class = RecipeSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title", "description", "ingredients"]
    ordering_fields = ["created_at", "prep_minutes", "cook_minutes"]
    ordering = ["-created_at"]


class RecipeDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = Recipe.objects.prefetch_related("tags").all()
    serializer_class = RecipeSerializer