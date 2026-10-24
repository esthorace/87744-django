from django.contrib.auth.decorators import login_not_required
from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import CustomLoginView, home, login_view, logout_view

app_name = "core"

urlpatterns = [
    path("", login_not_required(home), name="home"),
    # path("login/", login_view, name="login"),
    path("login/", CustomLoginView.as_view(), name="login"),
    # path("logout/", logout_view, name="logout"),
    path("logout/", LogoutView.as_view(template_name="core/logout.html"), name="logout"),
]
