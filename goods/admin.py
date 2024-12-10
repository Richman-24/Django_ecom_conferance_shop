from django.contrib import admin

from goods.models import Category, Comment, Product


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


@admin.register(Comment)  
class AdminComment(admin.ModelAdmin):  
    #list_display = ("user", "product_link", "created_at", "comment")
    list_display = ("product", "author", "created_at", "text", "is_published")
    list_editable = ("is_published",)  
    list_filter = ("author", "product") 

    # def product_link(self, obj):  
    #     return mark_safe(  
    #         f'<a href="{obj.product.get_absolute_url()}">{obj.product.title}</a>'  
    #     )  

    # product_link.allow_tags = True