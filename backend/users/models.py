from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(verbose_name='Email',
                              max_length=settings.EMAIL_LENGTH, unique=True)
    username = models.CharField(verbose_name='Имя пользователя',
                                max_length=settings.NAME_LENGTH, unique=True)
    first_name = models.CharField(verbose_name='Имя',
                                  max_length=settings.NAME_LENGTH)
    last_name = models.CharField(verbose_name='Фамилия',
                                 max_length=settings.NAME_LENGTH)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username', 'first_name', 'last_name')

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                name='only_one_follow_constraint',
                fields=['user', 'author']
            )
        ]
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    def __str__(self):
        return f'{self.user.username} подписался на {self.author.username}'
