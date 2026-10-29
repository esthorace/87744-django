__all__ = ["VendedorCreate", "VendedorDetail", "VendedorList", "VendedorUpdate"]

from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.db.models.query import QuerySet
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from ..forms import VendedorForm
from ..models import Vendedor


class VendedorList(ListView):
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


class VendedorDetail(DetailView):
    model = Vendedor
    context_object_name = "vendedor"


class VendedorCreate(SuccessMessageMixin, CreateView):
    model = Vendedor
    form_class = VendedorForm
    success_url = reverse_lazy("ventas:vendedor_list")
    # template_name = "ventas/vendedor_form.html"  -> por default busca <nombremodelo_form.html>
    success_message = "El vendedor se ha creado exitosamente"


class VendedorUpdate(SuccessMessageMixin, UpdateView):
    model = Vendedor
    form_class = VendedorForm
    success_url = reverse_lazy("ventas:vendedor_list")
    # template_name = "ventas/vendedor_form.html"  -> por default busca <nombremodelo_form.html>
    success_message = "El vendedor se ha editado exitosamente"
