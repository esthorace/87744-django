from django.urls import path

from . import views

app_name = "ventas"

urlpatterns = [
    path("", views.home, name="home"),
    path("categoria/list/", views.categoria_list, name="categoria_list"),
]
