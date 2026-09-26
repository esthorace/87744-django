from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import F, Q

from .categoria import Categoria
from .proveedor import Proveedor


class Producto(models.Model):
    nombre = models.CharField(unique=True)
    descripcion = models.TextField(blank=True)
    precio_costo = models.DecimalField(max_digits=10, decimal_places=2)
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.FloatField(default=0)
    codigo_barras = models.CharField(max_length=50, null=True, blank=True, unique=True)

    categoria = models.ForeignKey(
        Categoria, on_delete=models.SET_NULL, null=True, blank=True, related_name="productos"
    )
    proveedor = models.ForeignKey(
        Proveedor, on_delete=models.SET_NULL, null=True, blank=True, related_name="productos"
    )

    def __str__(self) -> str:
        return f"{self.nombre} (${self.precio_venta})"

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"

        constraints = (
            models.CheckConstraint(
                condition=Q(stock__gte=0),
                name="producto_stock_no_negativo",
            ),
            models.CheckConstraint(
                condition=Q(precio_costo__gte=0),
                name="producto_precio_costo_no_negativo",
            ),
            models.CheckConstraint(
                condition=Q(precio_venta__gte=0),
                name="producto_precio_venta_no_negativo",
            ),
            models.CheckConstraint(
                condition=Q(precio_venta__gte=F("precio_costo")),
                name="producto_precio_mayor_o_igual_costo",
            ),
        )

    def clean(self):
        super().clean()
        if (
            self.precio_venta is not None
            and self.precio_costo is not None
            and self.precio_venta < self.precio_costo
        ):
            raise ValidationError(
                {"precio_venta": "El precio de venta no puede ser menor que el precio de costo"}
            )
