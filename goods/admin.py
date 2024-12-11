from django.contrib import admin

from goods.models import Category, Favorite, Product

class FavoriteTab(admin.TabularInline):
    model = Favorite
    fields = ("product", "product_description", "product_sell_price")
    readonly_fields = ("product", "product_description","product_sell_price")
    extra = 0

    def product_description(self, obj):
        return obj.product.description

    def product_sell_price(self, obj):
        return obj.product.sell_price
    
    product_description.short_description = "Описание продукта"
    product_sell_price.short_description = "Цена"

@admin.register(Category)
class AdminCategory(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ("name", "is_published")
    list_editable = ("is_published",)


@admin.register(Product)
class AdminProduct(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ("name", "amount", "price", "discount", "is_published")
    list_editable = ("price", "discount", "is_published")
    fields = (
        "category",
        "name",
        "slug",
        "description",
        "amount",
        ("price", "discount"),
        "rating",
        "is_published",
        "image",
    )

