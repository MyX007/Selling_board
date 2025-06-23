from django.contrib.auth.models import AbstractUser
from django.db import models
from config.settings import USER_ROLES


class User(AbstractUser):
    """Модель пользователя."""
    first_name = models.CharField(
        max_length=30, verbose_name="Имя"
    )
    last_name = models.CharField(
        max_length=50, verbose_name="Фамилия", null=True, blank=True
    )
    user_role = models.CharField(
        max_length=20, choices=USER_ROLES, verbose_name="Роль пользвателя", default="Пользователь"
    )
    phone = models.CharField(
        max_length=35, verbose_name="Телефон", blank=True, null=True
    )
    avatar = models.ImageField(
        upload_to="users/", null=True, blank=True, verbose_name="Аватар"
    )
    username = None
    email = models.EmailField(
        unique=True, verbose_name="E-mail"
    )
    city = models.CharField(
        max_length=100, verbose_name="Страна", blank=True, null=True
    )
    token = models.CharField(
        max_length=100, verbose_name="Токен", blank=True, null=True
    )
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []


    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
