from django.http import Http404
from django.db.models import Avg
from django.shortcuts import get_object_or_404

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
        context["title"] = self.object.name
        context["comment_count"] = self.object.comments.count()
        context["average_rating"] = self.object.comments.aggregate(Avg('rating'))['rating__avg']
        context["comment_form"] = CommentForm()  

        return context
