from django.urls import path

from goods.views import AddFavorite, CatalogView, DeleteFavorite, ProductView

app_name = "goods"

urlpatterns = [
    path("", CatalogView.as_view(), name="index"),
    path("<slug:category_slug>/", CatalogView.as_view(), name="catalog"),
    path("product/<slug:product_slug>/", ProductView.as_view(), name="product"),

    path(
        "product/<slug:product_slug>/add-favorite/",
        AddFavorite.as_view(),
        name="add_favorite",
    ),
    path(
        "product/<slug:product_slug>/delete-favorite/",
        DeleteFavorite.as_view(),
        name="delete_favorite",
    ),
]
