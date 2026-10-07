from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

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


def categoria_detail(request: HttpRequest, pk: int) -> HttpResponse:
    # try:
    #     categoria = Categoria.objects.get(pk=pk)
    # except Categoria.DoesNotExist:
    #     raise Http404("El producto no existe")
    categoria = get_object_or_404(Categoria, pk=pk)

    return render(request, "ventas/categoria_detail.html", {"categoria": categoria})


def categoria_update(request: HttpRequest, pk: int) -> HttpResponse:
    categoria = get_object_or_404(Categoria, pk=pk)

    if request.method == "GET":
        form = CategoriaForm(instance=categoria)
    if request.method == "POST":
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            return redirect("ventas:categoria_list")

    return render(request, "ventas/categoria_form.html", {"form": form})
