__all__ = ["ProductoCreate", "ProductoDelete", "ProductoDetail", "ProductoList", "ProductoUpdate"]


from typing import Any

from django.contrib.messages.views import SuccessMessageMixin
from django.db.models.query import QuerySet
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from core.search import SearchListMixin

from ..forms import ProductoForm
from ..models.producto import Producto

# class ProductoList(SearchListMixin, ListView):
#     model = Producto
#     context_object_name = "productos"  # -> por default es "object_list"
#     search_fields = ("nombre__icontains",)
#     # template_name = "ventas/producto_list.html"  -> por default busca <nombremodelo_list.html>


class ProductoList(ListView):
    model = Producto
    context_object_name = "productos"  # -> por default es "object_list"
    # template_name = "ventas/producto_list.html"  -> por default busca <nombremodelo_list.html>

    def get_queryset(self) -> QuerySet[Any, Any]:
        busqueda = self.request.GET.get("busqueda", "").strip()
        if busqueda:
            productos = Producto.objects.filter(nombre__icontains=busqueda)
        else:
            productos = Producto.objects.all()
        return productos


class ProductoCreate(SuccessMessageMixin, CreateView):
    model = Producto
    form_class = ProductoForm
    success_url = reverse_lazy("ventas:producto_list")
    # template_name = "ventas/producto_form.html"  -> por default busca <nombremodelo_form.html>
    success_message = "El producto se ha creado exitosamente"


class ProductoDetail(DetailView):
    model = Producto
    context_object_name = "producto"
    # template_name = "ventas/producto_detail.html"


class ProductoUpdate(SuccessMessageMixin, UpdateView):
    model = Producto
    form_class = ProductoForm
    success_url = reverse_lazy("ventas:producto_list")
    success_message = "El producto se ha editado exitosamente"


class ProductoDelete(SuccessMessageMixin, DeleteView):
    model = Producto
    success_url = reverse_lazy("ventas:producto_list")
    success_message = "El producto se ha eliminado"
