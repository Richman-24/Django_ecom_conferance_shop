from django.urls import path

from goods.views import CatalogView, ProductView

app_name = 'goods'

urlpatterns = [
    path('', CatalogView.as_view(), name='index'),
    path('<slug:category_slug>/', CatalogView.as_view(), name='catalog'),
    path('product/<slug:product_slug>/', ProductView.as_view(), name ='product' ),
]
