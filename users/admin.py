from django.contrib import admin
from django.contrib.auth import get_user_model

from carts.admin import CartTabAdmin
from favorites.admin import FavoriteTab
from orders.admin import OrderTabulareAdmin

User = get_user_model()


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["username", "first_name", "last_name", "email",]

    inlines = [FavoriteTab, CartTabAdmin, OrderTabulareAdmin]