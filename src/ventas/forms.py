from django import forms

from .models.categoria import Categoria
from .models.producto import Producto


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        # fields = ("nombre", "descripcion")
        fields = "__all__"


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = "__all__"
