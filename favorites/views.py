from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.shortcuts import redirect

from favorites.models import Favorite
from goods.models import Product

class AddFavorite(LoginRequiredMixin, View):
    def post(self, request, product_slug):
        if request.user.favorites.filter(product__slug = product_slug).exists():
            raise ValueError("Товар уже в избранном")
        
        Favorite.objects.create(
            user = request.user,
            product = Product.objects.get(slug=product_slug)
        )

        return redirect(
            "catalog:product", product_slug = product_slug
            )

class DeleteFavorite(LoginRequiredMixin, View):
    def post(self, request, product_slug):
        favorite_obj = request.user.favorites.filter(product__slug = product_slug).first()

        if not favorite_obj:
            raise ValueError("Товара нет в избранном")
        favorite_obj.delete()

        return redirect(
            "catalog:product",
            product_slug = product_slug
            )