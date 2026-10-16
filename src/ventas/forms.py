from django import forms

from .models.categoria import Categoria
from .models.producto import Producto


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        # fields = ("nombre", "descripcion")
        fields = "__all__"

    def clean_nombre(self) -> str:
        nombre = self.cleaned_data.get("nombre", "")
        if len(nombre) < 3:
            raise forms.ValidationError("El nombre debe contener al menos 3 caracteres")
        return nombre


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = "__all__"
