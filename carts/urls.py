from django.urls import path

from carts.views import CartAddView, CartRemoveView, UpdateCartView, CartView

app_name = 'carts'


urlpatterns = [
    path("", CartView.as_view(), name="cart"), 
    path("add_cart/<slug:product_slug>/", CartAddView.as_view(), name="add_cart"),  
    path("edit_cart/<slug:product_slug>/", UpdateCartView.as_view(), name="edit_cart"),  
    path("delete_cart/<slug:product_slug>/", CartRemoveView.as_view(), name="delete_cart",),
]
