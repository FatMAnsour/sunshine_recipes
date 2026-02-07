from django.db import models
from django.urls import reverse


class Tag(models.Model):
    name = models.CharField(max_length=30, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Recipe(models.Model):
    MOOD_CHOICES = [
        ("comfort", "Comfort"),
        ("energizing", "Energizing"),
        ("quick", "Quick"),
        ("light", "Light"),
        ("celebration", "Celebration"),
    ]

    title = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    mood = models.CharField(max_length=20, choices=MOOD_CHOICES)
    prep_minutes = models.PositiveIntegerField(default=10)
    cook_minutes = models.PositiveIntegerField(default=10)
    ingredients = models.TextField(help_text="One ingredient per line")
    steps = models.TextField(help_text="One step per line")
    tags = models.ManyToManyField(Tag, blank=True, related_name="recipes")

    is_favorite = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def total_minutes(self):
        return self.prep_minutes + self.cook_minutes

    def get_absolute_url(self):
        return reverse("recipes:detail", kwargs={"pk": self.pk})
