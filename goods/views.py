from django.http import Http404
from django.db.models import Avg
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, DetailView

from comments.forms import CommentForm
from goods.models import Category, Favorite, Product


class CatalogView(ListView):
    model = Product
    template_name = "goods/catalog.html"
    context_object_name = "goods"
    paginate_by = 4

    def get_queryset(self):
        category_slug = self.kwargs.get("category_slug", "all")
        if category_slug == "all":
            queryset = super().get_queryset()
        else:
            queryset = super().get_queryset().filter(category__slug=category_slug)
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
        return get_object_or_404(Product, slug=self.kwargs[self.slug_url_kwarg])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = f"CoffeeShop - {self.object.name}"
        context["comment_count"] = self.object.comments.count()
        context["average_rating"] = self.average_rating() #self.object.comments.aggregate(Avg('rating'))['rating__avg']
        context["is_favorite"] = self.is_favorite()
        context["comment_form"] = CommentForm()  

        return context

    def is_favorite(self):
        return self.request.user.favorites.filter(product=self.object).exists()

    def average_rating(self):
        rating = self.object.comments.aggregate(Avg('rating'))['rating__avg']
        if rating:
            return rating
        return "Пока нет оценок"

# Представления работы с избранным
class AddFavorite(View):
    def post(self, request, product_slug):
        if request.user.favorites.filter(product__slug = product_slug).exists():
            raise ValueError("Товар уже в избранном")
        
        Favorite.objects.create(
            user = request.user,
            product = Product.objects.get(slug=product_slug)
        )

        return redirect(
            "catalog:product", product_slug = product_slug
            )

class DeleteFavorite(View):
    def post(self, request, product_slug):
        favorite_obj = request.user.favorites.filter(product__slug = product_slug).first()
        print(favorite_obj)

        if not favorite_obj:
            raise ValueError("Товара нет в избранном")
        favorite_obj.delete()

        return redirect(
            "catalog:product",
            product_slug = product_slug
            )