from rest_framework import serializers
from .models import Recipe, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name"]


class RecipeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    total_minutes = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = [
            "id",
            "title",
            "description",
            "mood",
            "prep_minutes",
            "cook_minutes",
            "total_minutes",
            "ingredients",
            "steps",
            "is_favorite",
            "tags",
            "created_at",
            "updated_at",
        ]

    def get_total_minutes(self, obj):
        return obj.total_minutes()
