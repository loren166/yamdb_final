from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import EmailValidator
from django.db import models


class User(AbstractUser):
    """Модель пользователей."""

    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    ROLES = [
        (USER, 'user'),
        (MODERATOR, 'moderator'),
        (ADMIN, 'admin'),
    ]

    username = models.CharField(
        max_length=150,
        unique=True,
        verbose_name='Имя пользователя',
        validators=[
            UnicodeUsernameValidator(message="Некорректное имя пользователя")
        ],
    )

    email = models.EmailField(
        max_length=254,
        unique=True,
        verbose_name='Электронная почта',
        validators=[EmailValidator(message="Некорректный e-mail")],
    )

    first_name = models.CharField(
        max_length=150,
        blank=True,
        verbose_name='Имя',
    )

    last_name = models.CharField(
        max_length=150,
        blank=True,
        verbose_name='Фамилия',
    )

    bio = models.TextField(
        max_length=500,
        blank=True,
        verbose_name='Информация о себе',
    )

    role = models.CharField(
        max_length=15,
        choices=ROLES,
        default=USER,
        verbose_name='Роль пользователя',
    )

    @property
    def is_user(self):
        return self.role == self.USER

    @property
    def is_admin(self):
        return self.role == self.ADMIN

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
