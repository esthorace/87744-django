from django.core.exceptions import ValidationError
from django.db import models


class Proveedor(models.Model):
    nombre = models.CharField(unique=True)
    telefono = models.CharField(blank=True)
    email = models.EmailField(blank=True)

    def __str__(self) -> str:
        return self.nombre

    class Meta:
        verbose_name = "Proveedor"
        verbose_name_plural = "Proveedores"

    def clean(self) -> None:
        super().clean()
        telefono_limpio = self.telefono.strip() if self.telefono else ""
        email_limpio = self.email.strip() if self.email else ""

        if not telefono_limpio and not email_limpio:
            mensaje_error = "Debe proporcionar al menos un medio de contacto"
            raise ValidationError({"telefono": mensaje_error, "email": mensaje_error})
