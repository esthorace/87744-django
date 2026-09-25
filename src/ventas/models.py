from typing import Any

from django.db import models


class Categoria(models.Model):
    """Categoría de productos"""

    nombre = models.CharField(unique=True)
    descripcion = models.TextField(blank=True)

    def __str__(self) -> str:
        return self.nombre
