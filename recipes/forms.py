from django import forms
from .models import Recipe


class dish_pic(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = '__all__'
