from django.shortcuts import render, redirect
from . import models
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .forms import dish_pic


def upload_image(request):
    if request.method == 'POST':
        form = dish_pic(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        return redirect('recipe_form.html')
    else:
        form = dish_pic()
        context = {
            'form': form
        }
    return render(request, 'recipe_form.html', context)


def home(request):
    recipes = models.Recipe.objects.all()
    context = {
        'recipes': recipes
    }
    return render(request, 'recipes/home.html', context)


class RecipeListView(ListView):
    model = models.Recipe
    template_name = 'recipes/home.html'
    context_object_name = 'recipes'


class RecipeDetailView(DetailView):
    model = models.Recipe


class RecipeCreateView(LoginRequiredMixin, CreateView):
    model = models.Recipe
    fields = ['title', 'description', 'dish_pic']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class RecipeUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = models.Recipe
    fields = ['title', 'description', 'dish_pic']

    def test_func(self):
        recipe = self.get_object()
        return self.request.user == recipe.author

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class RecipeDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = models.Recipe
    success_url = reverse_lazy('recipes-home')

    def test_func(self):
        recipe = self.get_object()
        return self.request.user == recipe.author


def about(request):
    return render(request, 'recipes/about.html', {'title': 'about page'})
