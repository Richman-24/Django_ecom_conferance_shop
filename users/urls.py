from django.urls import include, path
from django.views.generic import TemplateView
from users import views

app_name = 'users'

urlpatterns = [
    path("login/", views.UserLoginView.as_view(), name='login'),
    path("logout/", views.logout, name='logout'),
    path('signup/', views.UserSignUp.as_view(), name='signup'),
    path('profile/', views.UserpPofile.as_view(), name='profile'),
]
