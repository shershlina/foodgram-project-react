import django_filters as filters
from recipes.models import Recipe


class RecipeFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = Recipe
        fields = '__all__'
