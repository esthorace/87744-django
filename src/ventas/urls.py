from django.urls import path
from django.views.generic import TemplateView

from .views import *

app_name = "ventas"

urlpatterns = [
    path("", TemplateView.as_view(template_name="ventas/home.html"), name="home"),
]

urlpatterns += [
    path("categoria/list/", categoria_list, name="categoria_list"),
    path("categoria/create/", categoria_create, name="categoria_create"),
    path("categoria/detail/<int:pk>", categoria_detail, name="categoria_detail"),
    path("categoria/update/<int:pk>", categoria_update, name="categoria_update"),
    path("categoria/delete/<int:pk>", categoria_delete, name="categoria_delete"),
]

urlpatterns += [
    path("producto/", ProductoList.as_view(), name="producto_list"),
    path("producto/create/", ProductoCreate.as_view(), name="producto_create"),
    path("producto/detail/<int:pk>", ProductoDetail.as_view(), name="producto_detail"),
    path("producto/update/<int:pk>", ProductoUpdate.as_view(), name="producto_update"),
    path("producto/delete/<int:pk>", ProductoDelete.as_view(), name="producto_delete"),
]
