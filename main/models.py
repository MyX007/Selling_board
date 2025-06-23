from django.db import models

from users.models import User


class Advertisement(models.Model):
    """ Модель объявления."""
    title = models.CharField(max_length=100, verbose_name="Название")
    description = models.CharField(max_length=255, verbose_name="Описание")
    price = models.PositiveIntegerField(verbose_name="Цена")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")



class Review(models.Model):
    """ Модель отзыва. """
    content = models.TextField(verbose_name="Отзыв")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор", null=True, blank=True)
    ads = models.ForeignKey(Advertisement, on_delete=models.CASCADE, verbose_name="Объявление", null=True, blank=True)
