from django.contrib import admin
from django.contrib.auth import get_user_model

from favorites.admin import FavoriteTab

User = get_user_model()


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["username", "first_name", "last_name", "email",]

    inlines = [FavoriteTab]