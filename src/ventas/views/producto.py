__all__ = ["ProductoCreate", "ProductoDelete", "ProductoDetail", "ProductoList", "ProductoUpdate"]


from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from ..forms import ProductoForm
from ..models.producto import Producto


class ProductoList(ListView):
    model = Producto
    context_object_name = "productos"  # -> por default es "object_list"
    # template_name = "ventas/producto_list.html"  -> por default busca <nombremodelo_list.html>


class ProductoCreate(CreateView):
    model = Producto
    form_class = ProductoForm
    success_url = reverse_lazy("ventas:producto_list")
    # template_name = "ventas/producto_form.html"  -> por default busca <nombremodelo_form.html>


class ProductoDetail(DetailView):
    model = Producto
    context_object_name = "producto"
    # template_name = "ventas/producto_detail.html"


class ProductoUpdate(UpdateView):
    model = Producto
    form_class = ProductoForm
    success_url = reverse_lazy("ventas:producto_list")


class ProductoDelete(DeleteView):
    model = Producto
    success_url = reverse_lazy("ventas:producto_list")
