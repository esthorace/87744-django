from django.db import models


class Categoria(models.Model):
    nombre = models.CharField(unique=True)
    descripcion = models.TextField(blank=True)

    def __str__(self) -> str:
        return self.nombre

    class Meta:
        verbose_name = "Categoría de Producto"
        verbose_name_plural = "Categorías de Productos"
