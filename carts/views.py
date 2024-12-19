from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.shortcuts import get_object_or_404, redirect, render

from .models import Cart, Product


class CartView(LoginRequiredMixin, View):
    """Класс для отображения страницы корзины."""

    def get(self, request):
        user_carts = Cart.objects.filter(user=request.user)
        context = {"carts": user_carts}
        return render(request, "carts/cart.html", context)


class CartAddView(View):
    """Класс для добавления товаров в корзину."""

    def post(self, request, product_slug):
        product = get_object_or_404(Product, slug=product_slug)
        user_cart, created = Cart.objects.get_or_create(user=request.user, product=product)

        if not created:
            user_cart.amount += 1
        user_cart.save()

        return redirect('goods:product', product_slug=product.slug)


class UpdateCartView(LoginRequiredMixin, View):
    def post(self, request, product_slug):
        product = get_object_or_404(Product, slug=product_slug)
        user_cart = get_object_or_404(Cart, user=request.user, product=product)

        action = request.POST.get('action')

        if action == 'increase':
            user_cart.amount += 1
        elif action == 'decrease':
            if user_cart.amount > 1:
                user_cart.amount -= 1
            else:
                user_cart.delete()
                return redirect('carts:cart')

        user_cart.save()
        return redirect('carts:cart')


class CartRemoveView(LoginRequiredMixin, View):
    """Класс для удаления товаров из корзины."""

    def post(self, request, product_slug):
        product = get_object_or_404(Product, slug=product_slug)
        user_cart = get_object_or_404(Cart, user=request.user, product=product)
        user_cart.delete()

        return redirect('carts:cart')