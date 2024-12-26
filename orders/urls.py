from django.urls import path

from orders.views import (
    OrderCreateView,
    OrderDetailView
)

app_name = 'orders'


urlpatterns = [
    path("create_order/", OrderCreateView.as_view(), name="create_order"),
    path("<int:order_id>/", OrderDetailView.as_view(), name="detail_order"), 
]
