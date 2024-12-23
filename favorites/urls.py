from django.urls import path

from favorites.views import AddFavorite, DeleteFavorite

app_name = "favorites"

urlpatterns = [
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