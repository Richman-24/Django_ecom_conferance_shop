from django.db import models

from django.contrib.auth import get_user_model
from django.db import models

from coffeeshop.constants import ADMIN_LENGTH_LIMIT
from goods.models import Product

User = get_user_model()


class Cart(models.Model):
    product = models.ForeignKey(
        to=Product,
        on_delete=models.CASCADE,
        related_name="carts",
        verbose_name="Продукт",
    )
    user = models.ForeignKey(
        to=User, on_delete=models.SET_NULL, null=True, related_name="carts", verbose_name="Автор комментария"
    )
    amount = models.DecimalField(
        default=2.5, max_digits=3, decimal_places=1, verbose_name="Количество товара"
    )
    session_key = models.CharField(max_length=32, null=True, blank=True, verbose_name="Ключ сессии")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        db_table = "cart"
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"
        ordering = ("user__username", "created_at")

    @property
    def cart_price(self):
        return round(self.product.sell_price * self.amount, 2)
    
    def __str__(self):
        return f"{self.user}|{self.product} - {self.amount}"
