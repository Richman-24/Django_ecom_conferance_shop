from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView

from users.forms import LoginForm, ProfileForm, SignUpForm


class UserLoginView(LoginView):
    template_name = "users/login.html"
    form_class = LoginForm

    def get_success_url(self):
        redirect_page = self.request.POST.get("next", None)
        if redirect_page and redirect_page != reverse("users:logout"):
            return redirect_page
        return reverse_lazy("index")


class UserSignUp(CreateView):
    template_name="users/signup.html"
    form_class = SignUpForm
    success_url = reverse_lazy("users:profile")

    def form_valid(self, form):
        user = form.instance
        if user:
            form.save()
            auth.login(self.request, user)
            return HttpResponseRedirect(self.get_success_url())


class UserpPofile(LoginRequiredMixin, UpdateView):
    template_name = "users/profile.html"
    form_class = ProfileForm
    success_url = reverse_lazy("users:profile")

    def get_object(self, queryset =None):
        return self.request.user
    
    def form_valid(self, form):
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Личный кабинет"
        context["purchases"] = self.request.user.orders.all()
        context["favorites"] = (favorite.product for favorite in self.request.user.favorites.all())
        return context

@login_required
def logout(request):
    if request.method == "POST":
        auth.logout(request)
        return redirect("index")
    return render(request, "users/loggout.html")