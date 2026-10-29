__all__ = [
    "ProveedorCreate",
    "ProveedorDelete",
    "ProveedorDetail",
    "ProveedorList",
    "ProveedorUpdate",
]

from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.db.models.query import QuerySet
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from core.mixins import StaffRequiredMixin

from ..forms import ProveedorForm
from ..models import Proveedor


class ProveedorList(ListView):
    model = Proveedor
    context_object_name = "proveedores"

    def get_queryset(self) -> QuerySet:
        busqueda = self.request.GET.get("busqueda", "").strip()
        proveedores = Proveedor.objects.all()
        if busqueda:
            proveedores = proveedores.filter(
                Q(nombre__icontains=busqueda)
                | Q(telefono__icontains=busqueda)
                | Q(email__icontains=busqueda)
            )
        return proveedores


class ProveedorDetail(DetailView):
    model = Proveedor
    context_object_name = "proveedor"


class ProveedorCreate(StaffRequiredMixin, SuccessMessageMixin, CreateView):
    model = Proveedor
    form_class = ProveedorForm
    success_url = reverse_lazy("ventas:proveedor_list")
    # template_name = "ventas/proveedor_form.html"  -> por default busca <nombremodelo_form.html>
    success_message = "El proveedor se ha creado exitosamente"


class ProveedorUpdate(StaffRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Proveedor
    form_class = ProveedorForm
    success_url = reverse_lazy("ventas:proveedor_list")
    # template_name = "ventas/proveedor_form.html"  -> por default busca <nombremodelo_form.html>
    success_message = "El proveedor se ha editado exitosamente"


class ProveedorDelete(StaffRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Proveedor
    success_url = reverse_lazy("ventas:proveedor_list")
    # template_name = "ventas/proveedor_confirm_delete.html"  -> por default busca <nombremodelo_confirm_delete.html>
    success_message = "El proveedor se ha eliminado"
