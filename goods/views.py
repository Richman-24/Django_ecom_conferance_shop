from django.http import Http404
from django.db.models import Avg, Count

from django.views.generic import ListView, DetailView

from comments.forms import CommentForm
from goods.models import Category, Product


class CatalogView(ListView):
    model = Product
    template_name = "goods/catalog.html"
    context_object_name = "goods"
    paginate_by = 4

    def get_queryset(self):
        category_slug = self.kwargs.get("category_slug", "all")
        queryset = (
            super()
            .get_queryset()
            .filter(is_published=True, amount__gt=0)
            .select_related("category")
            .prefetch_related("comments")
            .annotate(
                average_rating=Avg("comments__rating"), comments_count=Count("comments")
            )
        )

        if category_slug != "all":
            queryset = queryset.filter(category__slug=category_slug)
            if not queryset.exists():
                raise Http404()
            self.title_obj = f"- {queryset[0].category.name}"

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "CoffeeShop Каталог"
        context["categories"] = Category.objects.all()
        context["slug_url"] = self.kwargs.get("category_slug")
        return context


class ProductView(DetailView):
    template_name = "goods/product.html"
    slug_url_kwarg = "product_slug"
    context_object_name = "product"

    def get_object(self, queryset=None):
        queryset = (Product.objects
        .prefetch_related("comments__author")
        .annotate(average_rating=Avg("comments__rating"))
        )
        return queryset.get(slug=self.kwargs[self.slug_url_kwarg])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = f"CoffeeShop - {self.object.name}"
        context["is_favorite"] = self.is_favorite()
        context["comment_form"] = CommentForm()

        return context

    def is_favorite(self):
        if self.request.user.is_authenticated:
            return self.request.user.favorites.filter(product=self.object).exists()
        return None
