from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from .forms import CategoriaForm
from .models.categoria import Categoria


def home(request: HttpRequest) -> HttpResponse:
    return render(request, "ventas/home.html")


def categoria_list(request: HttpRequest) -> HttpResponse:
    categorias = Categoria.objects.all()
    return render(request, "ventas/categoria_list.html", {"categorias": categorias})


def categoria_create(request: HttpRequest) -> HttpResponse:
    if request.method == "GET":
        form = CategoriaForm()
    if request.method == "POST":
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("ventas:categoria_list")

    return render(request, "ventas/categoria_form.html", {"form": form})
