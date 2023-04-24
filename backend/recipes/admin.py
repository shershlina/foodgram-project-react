from django.contrib import admin
from django.contrib.admin import display
from django.utils.safestring import mark_safe

from .models import (Favorite, Ingredient, IngredientRecipe, Recipe,
                     ShoppingCart, Tag)


class TagInLine(admin.TabularInline):
    model = Recipe.tags.through
    min_num = 1


class IngredientInLine(admin.TabularInline):
    model = Recipe.ingredients.through
    min_num = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'author', 'added_in_favorites',
                    'list_of_ingredients', 'list_of_tags', 'image')
    readonly_fields = ('added_in_favorites', 'list_of_ingredients',
                       'list_of_tags', 'image')
    list_filter = ('author', 'name', 'tags',)
    inlines = (TagInLine, IngredientInLine,)

    @display(description='Частота в избранном')
    def added_in_favorites(self, obj):
        return obj.favorites.count()

    @display(description='Ингредиенты')
    def list_of_ingredients(self, obj):
        return ', '.join([
            ingredients.name for ingredients
            in obj.ingredients.all()])

    @display(description='Теги')
    def list_of_tags(self, obj):
        return ', '.join([
            tags.name for tags
            in obj.tags.all()])

    @display(description='Изображение')
    def image(self, obj):
        if obj.image.exists():
            return mark_safe(f'<img src={obj.image.url} '
                             f'width="80" height="60">')
        return None


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit',)
    list_filter = ('name',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug',)


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe',)


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe',)


@admin.register(IngredientRecipe)
class IngredientRecipeAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'ingredient', 'amount',)
