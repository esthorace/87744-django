from django.urls import path

from . import views

app_name = "ventas"

urlpatterns = [
    path("", views.home, name="home"),
]

urlpatterns += [
    path("categoria/list/", views.categoria_list, name="categoria_list"),
    path("categoria/create/", views.categoria_create, name="categoria_create"),
    path("categoria/detail/<int:pk>", views.categoria_detail, name="categoria_detail"),
    path("categoria/update/<int:pk>", views.categoria_update, name="categoria_update"),
    path("categoria/delete/<int:pk>", views.categoria_delete, name="categoria_delete"),
]

urlpatterns += [
    path("producto/", views.ProductoList.as_view(), name="producto_list"),
    path("producto/create/", views.ProductoCreate.as_view(), name="producto_create"),
    # path("producto/detail/<int:pk>", views.producto_detail, name="producto_detail"),
    # path("producto/update/<int:pk>", views.producto_update, name="producto_update"),
    # path("producto/delete/<int:pk>", views.producto_delete, name="producto_delete"),
]
