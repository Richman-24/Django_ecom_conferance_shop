from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import RedirectView
from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", RedirectView.as_view(url="catalog/", permanent=True), name="index"),
    path("catalog/", include("goods.urls", namespace="catalog")),
    path("carts/", include("carts.urls", namespace="carts")),
    path("comment/", include("comments.urls", namespace="comments")),
    path("favorite/", include("favorites.urls", namespace="favorite")),
    path("users/", include("users.urls", namespace="users")),
    path("orders/", include("orders.urls", namespace="orders")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
