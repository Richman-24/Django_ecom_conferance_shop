from django.contrib.auth import get_user_model
from django.db import models

from coffeeshop.constants import ADMIN_LENGTH_LIMIT
from goods.models import Product

User = get_user_model()


class Comment(models.Model):
    product = models.ForeignKey(
        to=Product,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Продукт",
    )
    author = models.ForeignKey(
        to=User, on_delete=models.SET_NULL, null=True, related_name="comments", verbose_name="Автор комментария"
    )
    rating = models.DecimalField(
        default=2.5, max_digits=3, decimal_places=1, verbose_name="Оценка товара"
    )
    text = models.TextField(blank=True, verbose_name="Текст комментария")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    is_published = models.BooleanField(default=True, verbose_name="Показывать")

    class Meta:
        db_table = "comment"
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
        ordering = ("product", "created_at")

    def __str__(self):
        return f"{self.author}|{self.product} - {self.text[:ADMIN_LENGTH_LIMIT]}"
