from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name',
                    'recipe_count', 'follows_count')
    search_fields = ('username', 'email')
    list_filter = ('email', 'first_name', 'last_name')
    ordering = ('username', )
    empty_value_display = '-пусто-'

    @admin.display(description='Рецепты пользователя')
    def recipe_count(self, obj):
        return obj.recipes.count()

    @admin.display(description='Подписчики пользователя')
    def follows_count(self, obj):
        return obj.following.count()
