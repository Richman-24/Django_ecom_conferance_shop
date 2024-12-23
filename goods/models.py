from django.db import models
from django.contrib.auth import get_user_model

from coffeeshop.constants import NAME_LENGTH_LIMIT

User = get_user_model()


class BaseGoodModel(models.Model):

    def upload_path(instance, filename):
        """Автоматически генерирует название папки для загрузки файла"""
        model_name = instance.__class__.__name__.lower()
        return f"{model_name}_images/{filename}"

    name = models.CharField(
        max_length=NAME_LENGTH_LIMIT, unique=True, verbose_name="Название"
    )
    slug = models.SlugField(
        max_length=NAME_LENGTH_LIMIT, unique=True, verbose_name="URL"
    )
    is_published = models.BooleanField(default=True, verbose_name="Отображать")
    image = models.ImageField(upload_to=upload_path)

    class Meta:
        abstract = True


class Category(BaseGoodModel):

    class Meta:
        db_table = "category"
        verbose_name = "категория"
        verbose_name_plural = "категории"

    def __str__(self):
        return f"{self.name}"


class Product(BaseGoodModel):
    description = models.TextField(blank=True, verbose_name="Описание")
    amount = models.PositiveSmallIntegerField(verbose_name="Количество на складе")
    price = models.DecimalField(
        default=0.00, max_digits=7, decimal_places=2, verbose_name="Цена"
    )
    discount = models.PositiveSmallIntegerField(default=0, verbose_name="Скидка в %")
    category = models.ForeignKey(
        to=Category,
        on_delete=models.PROTECT,
        related_name="categories",
        verbose_name="Категория",
    )

    class Meta:
        db_table = "product"
        verbose_name = "продукт"
        verbose_name_plural = "продукты"
        ordering = ("name",)

    def __str__(self):
        return f"{self.name} - {self.amount}"

    @property
    def sell_price(self):
        discount_amount = (self.price * self.discount) / 100
        return self.price - discount_amount

