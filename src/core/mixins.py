"""Mixins de autorización reutilizables para vistas basadas en clases."""

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied


class StaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Permite el acceso solo a usuarios autenticados con ``is_staff=True``.

    - Usuario anónimo: se redirige al login (``LoginRequiredMixin``).
    - Usuario autenticado sin ``is_staff``: responde 403 (``PermissionDenied``).

    Uso::

        class VendedorList(StaffRequiredMixin, ListView):
            ...
    """

    permission_denied_message = "Solo el personal del negocio puede acceder a esta sección."

    def test_func(self) -> bool:
        return bool(self.request.user.is_staff)

    def handle_no_permission(self):
        # Un usuario logueado pero sin permisos no debe volver al login
        # (evita bucles de redirección): se le niega el acceso con un 403.
        if self.request.user.is_authenticated:
            raise PermissionDenied(self.get_permission_denied_message())
        return super().handle_no_permission()
