from django.urls import path

from . import views

app_name = "ventas"

urlpatterns = [
    path("", views.home, name="home"),
    path("categoria/list/", views.categoria_list, name="categoria_list"),
    path("categoria/create/", views.categoria_create, name="categoria_create"),
    path("categoria/detail/<int:pk>", views.categoria_detail, name="categoria_detail"),
    path("categoria/update/<int:pk>", views.categoria_update, name="categoria_update"),
]
