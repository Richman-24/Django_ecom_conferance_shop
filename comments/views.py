from django.urls import reverse
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

from comments.forms import CommentForm
from comments.models import Comment
from goods.models import Product

# (Необходимо придумать структуру, чтобы обрабатывать
# ошибки при вводе коментариев)


class CommentMixin(LoginRequiredMixin):
    model = Comment

    def get_success_url(self):
        product = Product.objects.get(pk=self.object.product.id)
        return reverse(
            "catalog:product",
            kwargs={"product_slug": product.slug},
        )


class AddCommentView(CommentMixin, CreateView):
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
class EditCommentView(CommentMixin, UpdateView):
    form_class = CommentForm
    template_name = "comments/comment_edit.html"


# Добавить пермишн на проверку - только автор или админ
class DeleteCommentView(CommentMixin, DeleteView):
    template_name = "comments/comment_delete.html"
