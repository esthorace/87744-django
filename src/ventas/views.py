from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from .models.categoria import Categoria


def home(request: HttpRequest) -> HttpResponse:
    return render(request, "ventas/home.html")


def categoria_list(request: HttpRequest) -> HttpResponse:
    categorias = Categoria.objects.all()
    return render(request, "ventas/categoria_list.html", {"categorias": categorias})
