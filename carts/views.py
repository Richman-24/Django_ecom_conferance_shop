from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.shortcuts import get_object_or_404, redirect, render

from .models import Cart, Product


class CartView(LoginRequiredMixin, View):
    """Класс для отображения страницы корзины."""

    def get(self, request):
        user_carts = self.get_user_carts(request.user)
        recommended_products = self.get_recommended_products(user_carts)
        total_amount = user_carts.total_amount()
        total_price = user_carts.total_price()

        context = {
            "carts": user_carts,
            "recommended_products": recommended_products,
            "total_amount": total_amount,
            "total_price": total_price
        }
        return render(request, "carts/cart.html", context)

    def get_user_carts(self, user):
        """Получить корзину пользователя."""
        return Cart.objects.filter(user=user)

    def get_recommended_products(self, user_carts):
        """
        Рекомендательный алгоритм.
        Сейчас - продукты, которых нет в корзине пользователя.
        """
        all_products = Product.objects.all()
        cart_product_slugs = user_carts.values_list('product__slug', flat=True)
        return all_products.exclude(slug__in=cart_product_slugs)


class CartAddView(LoginRequiredMixin, View):
    """Класс для добавления товаров в корзину."""

    def post(self, request, product_slug):
        product = get_object_or_404(Product, slug=product_slug)
        user_cart, created = Cart.objects.get_or_create(user=request.user, product=product)

        if not created:
            user_cart.amount += 1
        user_cart.save()

        referer = request.META.get('HTTP_REFERER', 'goods:product')

        return redirect(referer)


class UpdateCartView(LoginRequiredMixin, View):
    def post(self, request, product_slug):
        product = get_object_or_404(Product, slug=product_slug)
        user_cart = get_object_or_404(Cart, user=request.user, product=product)

        action = request.POST.get('action')

        if action == 'increase':
            user_cart.amount += 1
            user_cart.save()
        elif action == 'decrease':
            if user_cart.amount > 1:
                user_cart.amount -= 1
                user_cart.save()
            else:
                user_cart.delete()

        return redirect('carts:cart')


class CartRemoveView(LoginRequiredMixin, View):
    """Класс для удаления товаров из корзины."""

    def post(self, request, product_slug):
        product = get_object_or_404(Product, slug=product_slug)
        user_cart = get_object_or_404(Cart, user=request.user, product=product)
        user_cart.delete()

        return redirect('carts:cart')


class ClearUserCartView(LoginRequiredMixin, View):
    """Класс для полного удаления всех товаров из корзины пользователя."""

    def post(self, request):
        queryset = request.user.carts.all()
        queryset.delete()

        return redirect('carts:cart')