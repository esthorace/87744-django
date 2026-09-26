from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.db.models import F

from .models import Categoria, Producto, Proveedor


class StockBajoFilter(admin.SimpleListFilter):
    title = "nivel de stock"
    parameter_name = "nivel_stock"

    def lookups(self, request, model_admin):
        return (
            ("sin_stock", "Sin stock (0)"),
            ("bajo", "Stock bajo (< 10)"),
        )

    def queryset(self, request, queryset):
        if self.value() == "sin_stock":
            return queryset.filter(stock=0)
        if self.value() == "bajo":
            return queryset.filter(stock__lt=10, stock__gt=0)
        return queryset


class MargenNegativoFilter(admin.SimpleListFilter):
    title = "margen"
    parameter_name = "margen"

    def lookups(self, request, model_admin):
        return (("negativo", "Precio venta = costo (margen 0)"),)

    def queryset(self, request, queryset):
        if self.value() == "negativo":
            return queryset.filter(precio_venta=F("precio_costo"))
        return queryset


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "cantidad_productos")
    search_fields = ("nombre",)
    ordering = ("nombre",)

    @admin.display(description="Productos")
    def cantidad_productos(self, obj):
        return obj.productos.count()


@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ("nombre", "telefono", "email", "cantidad_productos")
    search_fields = ("nombre", "telefono", "email")
    ordering = ("nombre",)

    @admin.display(description="Productos")
    def cantidad_productos(self, obj):
        return obj.productos.count()


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = (
        "categoria",
        "nombre",
        "proveedor",
        "precio_costo",
        "precio_venta",
        "margen",
        "stock",
    )
    list_display_links = ("nombre",)
    list_filter = ("categoria", "proveedor", StockBajoFilter, MargenNegativoFilter)
    search_fields = (
        "categoria__nombre",
        "nombre",
    )
    ordering = ("nombre",)
    list_select_related = ("categoria", "proveedor")
    autocomplete_fields = ("categoria", "proveedor")
    list_per_page = 50
    readonly_fields = ("margen",)

    fieldsets = (
        (None, {"fields": ("nombre", "descripcion", "codigo_barras")}),
        ("Precios y stock", {"fields": ("precio_costo", "precio_venta", "margen", "stock")}),
        ("Relaciones", {"fields": ("categoria", "proveedor")}),
    )

    @admin.display(description="Margen")
    def margen(self, obj):
        if obj.precio_costo is None or obj.precio_venta is None:
            return "-"
        return obj.precio_venta - obj.precio_costo
