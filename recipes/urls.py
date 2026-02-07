from django.urls import path
from . import views


app_name = "recipes"

urlpatterns = [
    path("", views.RecipeListView.as_view(), name="list"),
    path("today/", views.TodaysPickView.as_view(), name="todays_pick"),
    path("meal-plan/print/", views.WeeklyMealPlanPrintView.as_view(), name="meal_plan_print"),

    path("new/", views.RecipeCreateView.as_view(), name="create"),
    path("<int:pk>/", views.RecipeDetailView.as_view(), name="detail"),
    path("<int:pk>/edit/", views.RecipeUpdateView.as_view(), name="update"),
    path("<int:pk>/delete/", views.RecipeDeleteView.as_view(), name="delete"),
    path("<int:pk>/favorite/", views.toggle_favorite, name="toggle_favorite"),
]
