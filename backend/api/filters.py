from django.db.models import Q
from django_filters.rest_framework import filters, FilterSet

from recipes.models import Ingredient, Recipe, Tag


class IngredientFilter(FilterSet):
    name = filters.CharFilter(method='filter_by_name')

    class Meta:
        model = Ingredient
        fields = ('name',)

    def filter_by_name(self, queryset, name, value):
        queryset = queryset.filter(Q(name__istartswith=value))
        return queryset


class RecipeFilter(FilterSet):
    tags = filters.ModelMultipleChoiceFilter(
        queryset=Tag.objects.all(),
        field_name='tags__slug',
        to_field_name='slug'
    )
    is_favorited = filters.BooleanFilter(method='filter_is_favorited')
    is_in_shopping_cart = filters.BooleanFilter(
        method='filter_is_in_shopping_cart')

    class Meta:
        model = Recipe
        fields = ('tags', 'author',)

    def filter_is_favorited(self, queryset, name, value):
        if value and not self.request.user.is_anonymous:
            return queryset.filter(favorites__user=self.request.user)
        return queryset

    def filter_is_in_shopping_cart(self, queryset, name, value):
        if value and not self.request.user.is_anonymous:
            return queryset.filter(shopping_cart__user=self.request.user)
        return queryset
