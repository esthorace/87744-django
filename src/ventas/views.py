from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import CategoriaForm, ProductoForm
from .models.categoria import Categoria
from .models.producto import Producto


def home(request: HttpRequest) -> HttpResponse:
    return render(request, "ventas/home.html")


def categoria_list(request: HttpRequest) -> HttpResponse:
    categorias = Categoria.objects.all()
    return render(request, "ventas/categoria_list.html", {"categorias": categorias})


class ProductoList(ListView):
    model = Producto
    # context_object_name = "productos"  -> por default es "object_list"
    # template_name = "ventas/producto_list.html"  -> por default busca <nombremodelo_list.html>


def categoria_create(request: HttpRequest) -> HttpResponse:
    if request.method == "GET":
        form = CategoriaForm()
    if request.method == "POST":
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("ventas:categoria_list")

    return render(request, "ventas/categoria_form.html", {"form": form})


class ProductoCreate(CreateView):
    model = Producto
    form_class = ProductoForm
    success_url = reverse_lazy("ventas:producto_list")
    # template_name = "ventas/producto_form.html"  -> por default busca <nombremodelo_form.html>


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


def categoria_delete(request: HttpRequest, pk: int) -> HttpResponse:
    categoria = get_object_or_404(Categoria, pk=pk)

    if request.method == "POST":
        categoria.delete()
        return redirect("ventas:categoria_list")

    return render(request, "ventas/categoria_confirm_delete.html", {"categoria": categoria})
