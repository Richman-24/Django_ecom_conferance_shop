from django.contrib import admin

from goods.models import Category, Product


@admin.register(Category)
class AdminCategory(admin.ModelAdmin):
    prepopulated_fields = {"slug":("name",)}
    list_display=("name", "is_published")
    list_editable=("is_published",)


@admin.register(Product)
class AdminProduct(admin.ModelAdmin):
    prepopulated_fields = {"slug":("name",)}
    list_display=("name", "amount", "price", "discount", "is_published")
    list_editable=("price", "discount", "is_published")
    fields = ("category", "name", "slug", "description", "amount", ("price", "discount"), "rating", "is_published", "image")