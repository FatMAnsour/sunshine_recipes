from django import forms
from .models import Recipe, Tag


class RecipeForm(forms.ModelForm):
    tags_text = forms.CharField(
        required=False,
        help_text="Comma-separated (e.g. pasta, vegan, spicy)",
        widget=forms.TextInput(attrs={"placeholder": "pasta, vegan, spicy"}),
        label="Tags",
    )

    class Meta:
        model = Recipe
        fields = [
            "title",
            "description",
            "mood",
            "prep_minutes",
            "cook_minutes",
            "ingredients",
            "steps",
            "is_favorite",
        ]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 3}),
            "ingredients": forms.Textarea(attrs={"rows": 6}),
            "steps": forms.Textarea(attrs={"rows": 6}),
        }

    def __init__(self, *args, **kwargs):
        instance = kwargs.get("instance")
        super().__init__(*args, **kwargs)
        # ========
        for name, field in self.fields.items():
         if hasattr(field.widget, "attrs"):
            base = field.widget.attrs.get("class", "")
            if "form-control" not in base and field.widget.__class__.__name__ not in ["CheckboxInput"]:
                field.widget.attrs["class"] = (base + " form-control").strip()

        self.fields["mood"].widget.attrs["class"] = "form-select"
        self.fields["is_favorite"].widget.attrs["class"] = "form-check-input"
        # ========
        if instance and instance.pk:
            self.fields["tags_text"].initial = ", ".join(
                t.name for t in instance.tags.all()
            )

    def save(self, commit=True):
        recipe = super().save(commit=commit)
        tags_raw = self.cleaned_data.get("tags_text", "")
        tag_names = [t.strip().lower() for t in tags_raw.split(",") if t.strip()]

        if commit:
            recipe.tags.clear()
            for name in tag_names:
                tag, _ = Tag.objects.get_or_create(name=name)
                recipe.tags.add(tag)
        return recipe
