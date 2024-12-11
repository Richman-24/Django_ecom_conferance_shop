from django.urls import path

from carts.views import AddCartView, DeleteCartView, EditCartView

app_name = 'carts'


urlpatterns = [
    path("add/<int:pk>/", AddCartView.as_view(), name="add_cart"),  
    path("edit/<int:pk>/", EditCartView.as_view(), name="edit_cart"),  
    path("delete/<int:pk>/", DeleteCartView.as_view(), name="delete_cart",),
]
