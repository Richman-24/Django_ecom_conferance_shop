from django.urls import reverse
from django.views.generic import CreateView, UpdateView, DeleteView

from carts.models import Cart
from goods.models import Product


# (Необходимо придумать структуру, чтобы обрабатывать
# ошибки при вводе коментариев)

class CartMixin:
    model = Cart

    def get_success_url(self):
        product = Product.objects.get(pk=self.object.product.id)
        return reverse(
            "catalog:product",
            kwargs={"product_slug": product.slug},
        )


class AddCartView(CartMixin, CreateView):
    template_name = "goods/product.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.product = Product.objects.get(pk=self.kwargs.get("pk"))
        return super().form_valid(form)

    def form_invalid(self, form):
        response = super().form_invalid(form)
        return response


# Добавить пермишн на проверку - только автор или админ
class EditCartView(CartMixin, UpdateView):
    template_name = "carts/Cart_edit.html"


# Добавить пермишн на проверку - только автор или админ
class DeleteCartView(CartMixin, DeleteView):
    template_name = "carts/Cart_delete.html"
