from django.contrib import messages
from django.db import transaction
from django.forms import ValidationError
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

from orders.forms import CreateOrderForm
from orders.models import Order, OrderItem


class OrderCreateView(LoginRequiredMixin, CreateView):
    model = Order
    template_name = "orders/create_order.html"
    form_class = CreateOrderForm
    success_url = reverse_lazy("users:profile")

    def form_valid(self, form):
        try:
            with transaction.atomic():
                order = form.save(commit=False)
                order.user = self.request.user
                order.save()

                cart_items = self.get_cart_items()
                order_items = []

                for item in cart_items:
                    product = item.product
                    amount = item.amount

                    if product.amount < amount:
                        raise ValidationError(
                            f"Недостаточное количество товара {product.name} на складе. В наличии - {product.amount}"
                        )

                    order_items.append(
                        OrderItem(
                            order=order,
                            price=product.sell_price,
                            product=product,
                            amount=amount,
                        )
                    )

                    product.amount -= amount
                    product.save()

                OrderItem.objects.bulk_create(order_items)
                cart_items.delete()

                messages.success(self.request, "Заказ оформлен!")
                return redirect(self.success_url)

        except ValidationError as e:
            messages.error(self.request, str(e))
            return redirect("orders:create_order")

    def form_invalid(self, form):
        messages.error(self.request, "Какая-то ошибка!")
        return redirect("orders:create_order")

    def get_cart_items(self):
        return self.request.user.carts.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_carts = self.get_cart_items()
        context["carts"] = user_carts
        context["total_price"] = user_carts.total_price()
        context["total_amount"] = user_carts.total_amount()
        return context


class OrderDetailView(LoginRequiredMixin, DetailView):
    template_name = "orders/order_detail.html"
    pk_url_kwarg = "order_id"
    context_object_name = "order"

    def get_object(self, queryset=None):
        return get_object_or_404(Order, id=self.kwargs[self.pk_url_kwarg])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = f"CoffeeShop - {self.object}"
        return context


class OrderRemoveView(LoginRequiredMixin, DeleteView):
    template_name = "orders/order_delete.html"
    pk_url_kwarg = "order_id"
    context_object_name = 'order'
    success_url = reverse_lazy("users:profile")
    model = Order

    def post(self, request, *args, **kwargs):
        # Дальнейшая доработка зависит от политики компании: 
        # Отмена отправляется к менеджеру на подтверждение
        #   - Если менеджер подтверждает
        #     - оплата возвращается клиенту
        #     - количество товара на складе увеличивается

        messages.success(self.request, "Заказ отменен!")
        return super().post(request, *args, **kwargs)