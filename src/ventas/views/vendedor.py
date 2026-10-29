__all__ = ["VendedorList"]

from django.db.models import Q
from django.db.models.query import QuerySet
from django.views.generic import ListView

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
