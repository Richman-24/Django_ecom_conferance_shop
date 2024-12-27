from django.contrib import admin

from orders.models import Order, OrderItem


class OrderItemTabulareAdmin(admin.TabularInline):
    model = OrderItem
    fields = "product", "price", "amount"
    search_fields = ("product",)
    extra = 0


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("order", "product", "amount", "price")
    readonly_fields = ("order", "product", "amount", "price")


class OrderTabulareAdmin(admin.TabularInline):
    model = Order
    fields = (
        "created_at",
        "required_delivery",
        "status",
        "is_paid",
    )
    readonly_fields = ("created_at",)
    extra = 0



@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("user", "status", "created_at")
    readonly_fields = ("user", "created_at")
