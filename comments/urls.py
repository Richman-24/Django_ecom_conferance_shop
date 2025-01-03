from django.urls import path

from comments.views import AddCommentView, DeleteCommentView, EditCommentView

app_name = 'comments'

urlpatterns = [
    path("add/<int:pk>/", AddCommentView.as_view(), name="add_comment"),  
    path("edit/<int:pk>/", EditCommentView.as_view(), name="edit_comment"),  
    path("delete/<int:pk>/", DeleteCommentView.as_view(), name="delete_comment",),
]
