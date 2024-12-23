from django.contrib import admin

from favorites.models import Favorite


class FavoriteTab(admin.TabularInline):
    model = Favorite
    fields = ("product", "product_description", "product_sell_price")
    readonly_fields = ("product", "product_description", "product_sell_price")
    extra = 0

    def product_description(self, obj):
        return obj.product.description

    def product_sell_price(self, obj):
        return obj.product.sell_price

    product_description.short_description = "Описание продукта"
    product_sell_price.short_description = "Цена"
