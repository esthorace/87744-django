from django.contrib import admin

from ventas.models import Categoria, Producto, Proveedor

admin.site.register(Categoria)
admin.site.register(Proveedor)

# admin.site.register(Producto)


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ("categoria", "nombre", "precio_costo", "precio_venta", "stock")
    list_filter = ("categoria",)
    ordering = ("nombre",)
    search_fields = ("categoria__nombre", "nombre")
