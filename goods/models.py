from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

NAME_LENGTH_LIMIT = 64
ADMIN_LENGTH_LIMIT = 20


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
        ordering = ('name',)

    def __str__(self):
        return f"{self.name} - {self.amount}"

    @property
    def sell_price(self):
        discount_amount = (self.price * self.discount) / 100
        return self.price - discount_amount


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
        default=2.5, max_digits=2, decimal_places=1, verbose_name="Оценка товара"
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
