__all__ = ["categoria_create", "categoria_delete", "categoria_detail", "categoria_list", "categoria_update"]

from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from ..forms import CategoriaForm
from ..models.categoria import Categoria


def categoria_list(request: HttpRequest) -> HttpResponse:
    categorias = Categoria.objects.all()
    return render(request, "ventas/categoria_list.html", {"categorias": categorias})


def categoria_create(request: HttpRequest) -> HttpResponse:

    if request.method == "POST":
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("ventas:categoria_list")
    else:
        # ejecuta request de tipo GET y cualquier otro tipo
        form = CategoriaForm()

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

    if request.method == "POST":
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            return redirect("ventas:categoria_list")
    else:
        form = CategoriaForm(instance=categoria)
    return render(request, "ventas/categoria_form.html", {"form": form})


def categoria_delete(request: HttpRequest, pk: int) -> HttpResponse:
    categoria = get_object_or_404(Categoria, pk=pk)

    if request.method == "POST":
        categoria.delete()
        return redirect("ventas:categoria_list")

    return render(request, "ventas/categoria_confirm_delete.html", {"categoria": categoria})
