"""Búsqueda reutilizable (DRY) para listados CRUD.

El parámetro GET es siempre ``busqueda`` en todos los CRUD,
el parcial ``core/partials/search.html`` y las vistas comparten
estas constantes para no repetir lógica.
"""

from django.db.models import Q, QuerySet
from django.http import HttpRequest


def get_search_term(request: HttpRequest, param: str = "busqueda") -> str:
    """Devuelve el término de búsqueda limpio (``""`` si no hay)."""
    return request.GET.get(param, "").strip()


def filter_by_search(
    request: HttpRequest,
    queryset: QuerySet,
    *search_fields: str,
    param: str = "busqueda",
) -> QuerySet:
    """Filtra ``queryset`` con OR de ``__icontains`` sobre ``search_fields``.

    Uso en vistas basadas en función::

        categorias = filter_by_search(
            request, Categoria.objects.all(), "nombre__icontains"
        )
    """
    term = get_search_term(request, param)
    if not term or not search_fields:
        return queryset
    query = Q()
    for field in search_fields:
        query |= Q(**{field: term})
    return queryset.filter(query)


class SearchListMixin:
    """Mixin DRY para ``ListView`` con búsqueda por GET.

    Uso::

        class ProductoList(SearchListMixin, ListView):
            search_fields = ("nombre__icontains",)
    """

    search_fields: tuple[str, ...] = ("nombre__icontains",)
    search_param: str = "busqueda"

    def get_queryset(self):
        queryset = super().get_queryset()
        return filter_by_search(
            self.request,
            queryset,
            *self.search_fields,
            param=self.search_param,
        )
