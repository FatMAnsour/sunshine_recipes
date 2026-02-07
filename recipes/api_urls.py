from django.urls import path
from .views import RecipeListAPI, RecipeDetailAPI

urlpatterns = [
    path("recipes/", RecipeListAPI.as_view(), name="api-recipes"),
    path("recipes/<int:pk>/", RecipeDetailAPI.as_view(), name="api-recipe-detail"),
]
