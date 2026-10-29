__all__ = [
    "VendedorCreate",
    "VendedorDelete",
    "VendedorDetail",
    "VendedorList",
    "VendedorUpdate",
]

from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.db.models.query import QuerySet
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from core.mixins import StaffRequiredMixin

from ..forms import VendedorForm
from ..models import Vendedor


class VendedorList(StaffRequiredMixin, ListView):
    model = Vendedor
    context_object_name = "vendedores"

    def get_queryset(self) -> QuerySet:
        busqueda = self.request.GET.get("busqueda", "").strip()
        vendedores = Vendedor.objects.select_related("usuario")
        if busqueda:
            vendedores = vendedores.filter(
                Q(usuario__first_name__icontains=busqueda)
                | Q(usuario__last_name__icontains=busqueda)
                | Q(usuario__username__icontains=busqueda)
            )
        return vendedores


class VendedorDetail(StaffRequiredMixin, DetailView):
    model = Vendedor
    context_object_name = "vendedor"


class VendedorCreate(StaffRequiredMixin, SuccessMessageMixin, CreateView):
    model = Vendedor
    form_class = VendedorForm
    success_url = reverse_lazy("ventas:vendedor_list")
    # template_name = "ventas/vendedor_form.html"  -> por default busca <nombremodelo_form.html>
    success_message = "El vendedor se ha creado exitosamente"


class VendedorUpdate(StaffRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Vendedor
    form_class = VendedorForm
    success_url = reverse_lazy("ventas:vendedor_list")
    # template_name = "ventas/vendedor_form.html"  -> por default busca <nombremodelo_form.html>
    success_message = "El vendedor se ha editado exitosamente"


class VendedorDelete(StaffRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Vendedor
    success_url = reverse_lazy("ventas:vendedor_list")
    # template_name = "ventas/vendedor_confirm_delete.html"  -> por default busca <nombremodelo_confirm_delete.html>
    success_message = "El vendedor se ha eliminado"
