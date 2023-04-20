from django.contrib import admin
from django.db.models import Count

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name',
                    'recipe_count', 'follows_count')
    search_fields = ('username', 'email')
    list_filter = ('email', 'first_name', 'last_name')
    ordering = ('username', )
    empty_value_display = '-пусто-'

    def recipe_count(self, obj):
        return obj._recipe_count

    def follows_count(self, obj):
        return obj._follows_count

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(
            _recipe_count=Count('recipes', distinct=True),
            _follows_count=Count('following', distinct=True),
        )
        return queryset
