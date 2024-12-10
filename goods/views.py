from django.http import Http404
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from goods.forms import CommentForm
from goods.models import Category, Comment, Product


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

# Представления комментариев
# (Необходимо придумать структуру, чтобы обрабатывать
# ошибки при вводе коментариев)

class BaseCommentView:
    model = Comment

    def get_success_url(self):
        product = Product.objects.get(pk = self.object.product.id)
        return reverse(
            "catalog:product",
            kwargs = {"product_slug": product.slug},
        )


class AddCommentView(BaseCommentView, CreateView):  
    form_class = CommentForm
    template_name = "goods/product.html"

    def form_valid(self, form):  
        form.instance.author = self.request.user  
        form.instance.product = Product.objects.get(pk=self.kwargs.get("pk"))  
        return super().form_valid(form)
    
    def form_invalid(self, form):
        response = super().form_invalid(form)
        return response    


 # Добавить пермишн на проверку - только автор или админ
class EditCommentView(BaseCommentView, UpdateView): 
    form_class = CommentForm  
    template_name = "comments/comment_edit.html"  


# Добавить пермишн на проверку - только автор или админ
class DeleteCommentView(BaseCommentView, DeleteView):  
    template_name = "comments/comment_delete.html"