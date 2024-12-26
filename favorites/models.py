from django.db import models
from django.contrib.auth import get_user_model

from goods.models import Product

User = get_user_model()


class Favorite(models.Model):
    product = models.ForeignKey(
        to=Product,
        on_delete=models.CASCADE,
        related_name="favorites",
        verbose_name="Продукт",
    )
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name="favorites",
        verbose_name="Пользователь",
    )

    class Meta:
        db_table = "favorite"
        verbose_name = "Избранное"
        verbose_name_plural = "Избранные"
        ordering = ("user__username",)
        constraints = (
            models.UniqueConstraint(
                fields=("user", "product"), name="unique_favorite_product"
            ),
        )
