from django.conf import settings
from django.core.validators import MinValueValidator, RegexValidator
from django.db import models
from django.db.models import UniqueConstraint

from users.models import User


class Tag(models.Model):
    name = models.CharField(verbose_name='Название тега',
                            max_length=settings.CHAR_LENGTH, unique=True)
    color = models.CharField(verbose_name='HEX-код цвета',
                             max_length=7, unique=True,
                             validators=[RegexValidator(
                                 regex='^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$',
                                 message='Проверьте правильность HEX-кода'
                             )])
    slug = models.SlugField(verbose_name='Слаг',
                            max_length=settings.CHAR_LENGTH, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(verbose_name='Название',
                            max_length=settings.CHAR_LENGTH)
    measurement_unit = models.CharField(verbose_name='Единица измерения',
                                        max_length=settings.CHAR_LENGTH)

    class Meta:
        ordering = ('name',)
        constraints = [
            UniqueConstraint(
                fields=('name', 'measurement_unit'),
                name='unique_ingredient'
            ),
        ]
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'


class Recipe(models.Model):
    tags = models.ManyToManyField(Tag, through='TagRecipe',
                                  related_name='recipes',
                                  verbose_name='Тег')
    ingredients = models.ManyToManyField(Ingredient,
                                         through='IngredientRecipe',
                                         related_name='recipes',
                                         verbose_name='Ингредиент')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='recipes',
                               verbose_name='Автор')
    name = models.CharField(verbose_name='Название',
                            max_length=settings.CHAR_LENGTH)
    image = models.ImageField(verbose_name='Изображение',
                              upload_to='recipes/images/')
    text = models.TextField(verbose_name='Описание')
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления',
        validators=[MinValueValidator(
            1,
            message='Время приготовления должно отличаться от нуля')]
    )
    created = models.DateTimeField(verbose_name='Дата публикации',
                                   auto_now_add=True)

    class Meta:
        ordering = ('created',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class TagRecipe(models.Model):
    tag = models.ForeignKey(
        Tag,
        on_delete=models.SET_NULL,
        blank=True, null=True,
        verbose_name='Тег'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.SET_NULL,
        blank=True, null=True,
        verbose_name='Рецепт'
    )

    class Meta:
        verbose_name = 'Тег рецепта'
        verbose_name_plural = 'Теги рецепта'

    def __str__(self):
        return f'Тег "{self.tag}" у рецепта {self.recipe}'


class IngredientRecipe(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.SET_NULL,
        blank=True, null=True,
        related_name='recipe_ingredients',
        verbose_name='Ингредиент'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.SET_NULL,
        blank=True, null=True,
        related_name='recipe_ingredients',
        verbose_name='Рецепт'
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name='Кол-во ингредиента',
        validators=[MinValueValidator(
            1, message='Укажите верное кол-во ингредиента'
        )]
    )

    class Meta:
        verbose_name = 'Ингредиент рецепта'
        verbose_name_plural = 'Ингредиенты рецепта'
        constraints = [
            models.UniqueConstraint(
                fields=['ingredient', 'recipe'],
                name='unique_ingredient_in_recipe',
            )
        ]

    def __str__(self):
        return (f'Кол-во "{self.ingredient}" в рецепте "{self.recipe}":'
                f'{self.amount} {self.ingredient.measurement_unit}')


class UserRecipeBaseModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             verbose_name='Пользователь')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               verbose_name='Рецепт')

    class Meta:
        abstract = True
        constraints = [
            UniqueConstraint(name='only_unique_recipe_in_%(class)',
                             fields=['user', 'recipe'])
        ]
        ordering = ('recipe',)

    def __str__(self):
        return f'"{self.recipe}" добавлен пользователем {self.user}'


class Favorite(UserRecipeBaseModel):

    class Meta(UserRecipeBaseModel.Meta):
        default_related_name = 'favorites'
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'


class ShoppingCart(UserRecipeBaseModel):

    class Meta(UserRecipeBaseModel.Meta):
        default_related_name = 'shopping_cart'
        verbose_name = 'Рецепт в корзине'
        verbose_name_plural = 'Рецепты в корзине'
