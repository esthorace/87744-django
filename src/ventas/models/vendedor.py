from django.conf import settings
from django.db import models
from phonenumber_field.formfields import PhoneNumberField


class Vendedor(models.Model):
    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="vendedor"
    )
    telefono = PhoneNumberField(region="AR")
    foto_perfil = models.ImageField(null=True, blank=True, upload_to="vendedores/perfiles/")

    def __str__(self) -> str:
        return self.usuario.get_full_name() or self.usuario.username

    class Meta:
        verbose_name = "Vendedor"
        verbose_name_plural = "Vendedores"
