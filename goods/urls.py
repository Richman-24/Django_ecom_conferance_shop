from django.urls import include, path

from goods.views import AddCommentView, CatalogView, DeleteCommentView, EditCommentView, ProductView

app_name = 'goods'

urlpatterns = [
    path('', CatalogView.as_view(), name='index'),
    path('<slug:category_slug>/', CatalogView.as_view(), name='catalog'),
    path('product/<slug:product_slug>/', ProductView.as_view(), name ='product' ),

    path("comment/add/<int:pk>/", AddCommentView.as_view(), name="add_comment"),  
    path("comment/edit/<int:pk>/", EditCommentView.as_view(), name="edit_comment"),  
    path("comment/delete/<int:pk>/", DeleteCommentView.as_view(), name="delete_comment",),
]
