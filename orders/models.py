from django.db import models
from django.contrib.auth import get_user_model

from goods.models import Product

User = get_user_model()


class Order(models.Model):
    """Вся дополнительная информация о заказе."""

    class StatucChoices(models.TextChoices):
        CREATED = "C", "Ждёт оплаты"
        FORMING = "F", "Собирается"
        ON_DELIVERY = "D", "Передан в доставку"
        READY = "R", "Готов к выдаче"
        COURIER = "Z", "Передан курьеру"
        ISSUED = "I", "Выдан"

    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name="orders",
        verbose_name="Покупатель",
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата создания заказа"
    )
    is_paid = models.BooleanField(default=False, verbose_name="Заказ оплачен")
    required_delivery = models.BooleanField(
        default=False, verbose_name="Требуется доставка"
    )
    delivery_adress = models.CharField(
        max_length=256, verbose_name="Адрес доставки/ПВЗ"
    )
    status = models.CharField(
        max_length=1,
        choices=StatucChoices.choices,
        default="C",
        verbose_name="Статус заказа",
    )

    class Meta:
        db_table = "order"
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ("created_at",)

    def __str__(self):
        return f"Заказ от {self.created_at.date()} | № {self.pk:06}"


class OrderItem(models.Model):
    """Информация о проданном товаре в заказе."""

    order = models.ForeignKey(to=Order, on_delete=models.CASCADE, related_name='order_items', verbose_name="Заказ")
    product = models.ForeignKey(
        to=Product, on_delete=models.SET_DEFAULT, default=None, verbose_name="Товар"
    )
    amount = models.PositiveSmallIntegerField(default=1, verbose_name="Количество")
    price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Цена в момент заказа"
    )

    class Meta:
        db_table = "order_product"
        verbose_name = "Проданный товар"
        verbose_name_plural = "Проданные товары"
        ordering = ("order",)

    @property
    def order_item_price(self):
        return round(self.price * self.amount, 2)
    

    def __str__(self):
        return f"{self.product.name}: Количество {self.amount} ({self.order_item_price})"
