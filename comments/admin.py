from django.contrib import admin

from comments.models import Comment


@admin.register(Comment)
class AdminComment(admin.ModelAdmin):
    # list_display = ("user", "product_link", "created_at", "comment")
    list_display = ("product", "author", "created_at", "text", "is_published")
    list_editable = ("is_published",)
    list_filter = ("author", "product")

    # def product_link(self, obj):
    #     return mark_safe(
    #         f'<a href="{obj.product.get_absolute_url()}">{obj.product.title}</a>'
    #     )

    # product_link.allow_tags = True
