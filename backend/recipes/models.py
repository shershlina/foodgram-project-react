from django.core.validators import MinValueValidator, RegexValidator
from django.db import models
from django.db.models import UniqueConstraint

from users.models import User


class Tag(models.Model):
    name = models.CharField('Название тега', max_length=200, unique=True)
    color = models.CharField('HEX-код цвета', max_length=7, unique=True,
                             validators=[RegexValidator(
                                 regex='^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$',
                                 message='Проверьте правильность HEX-кода'
                             )])
    slug = models.SlugField('Слаг', max_length=200, unique=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField('Название', max_length=200)
    measurement_unit = models.CharField('Единица измерения', max_length=200)

    class Meta:
        ordering = ('name',)
        constraints = [
            UniqueConstraint(
                fields=('name', 'measurement_unit'),
                name='unique_ingredient'
            ),
        ]

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'


class Recipe(models.Model):
    tags = models.ManyToManyField(Tag, through='TagRecipe')
    ingredients = models.ManyToManyField(Ingredient,
                                         through='IngredientRecipe')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='recipes')
    name = models.CharField('Название', max_length=200)
    image = models.ImageField('Изображение', upload_to='recipes/')
    text = models.CharField(
        'Описание', max_length=1000,
        validators=[MinValueValidator(
            1, message='Добавьте описание или способ приготовления')])
    cooking_time = models.PositiveSmallIntegerField(
        'Время приготовления',
        validators=[MinValueValidator(
            1,
            message='Время приготовления должно быть больше 1 минуты')]
    )
    created = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return self.name


class TagRecipe(models.Model):
    tag = models.ForeignKey(
        Tag,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )

    def __str__(self):
        return f'Тег "{self.tag}" у рецепта {self.recipe}'


class IngredientRecipe(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='recipe_ingredients'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='recipe_ingredients'
    )
    amount = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(
            1, message='Укажите верное кол-во ингредиента'
        )]
    )

    def __str__(self):
        return (f'Кол-во "{self.ingredient}" в рецепте "{self.recipe}":'
                f'{self.amount} {self.ingredient.measurement_unit}')


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='favorites')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               related_name='favorites')

    class Meta:
        constraints = [
            UniqueConstraint(name='only_unique_favorite',
                             fields=['user', 'recipe'])
        ]

    def __str__(self):
        return f'Рецепт "{self.recipe}" добавлен в избранное.'


class ShoppingCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='shopping_cart')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               related_name='shopping_cart')

    class Meta:
        constraints = [
            UniqueConstraint(name='only_unique_recipe_in_cart',
                             fields=['user', 'recipe'])
        ]

    def __str__(self):
        return (f'Ингредиенты рецепта "{self.recipe}" '
                f'добавлены в список покупок.')
