from django.urls import path

from prueba import views

app_name = "prueba"

urlpatterns = [
    path("", views.home, name="home"),
    path("saludar/", views.saludar, name="saludar"),
    path("saludar/2/", views.saludar_2, name="saludar_2"),
    path("parametros/<str:nombre>/<str:apellido>/", views.parametros, name="parametros"),
    path("notas/", views.notas, name="notas"),
    path("cliente/list", views.cliente_list, name="cliente_list"),
]
