import re

from django import forms

from core.validators import ValidarTextoEspañol

from .models.categoria import Categoria
from .models.producto import Producto


class CategoriaForm(forms.ModelForm):
    nombre = forms.CharField(validators=[ValidarTextoEspañol(min_longitud=3)])
    descripcion = forms.CharField(
        widget=forms.Textarea,
        validators=[ValidarTextoEspañol(min_longitud=10)],
        required=False,
    )

    class Meta:
        model = Categoria
        # fields = ("nombre", "descripcion")
        fields = "__all__"

    def clean_nombre(self) -> str:
        nombre = self.cleaned_data.get("nombre", "")

        # Reemplaza múltiples espacios por uno solo y remueve espacios en los bordes
        nombre = re.sub(r"\s+", " ", nombre.strip())
        return nombre

    def clean_descripcion(self) -> str:
        descripcion = self.cleaned_data.get("descripcion", "")

        # Reemplaza múltiples espacios por uno solo y remueve espacios en los bordes
        descripcion = re.sub(r"\s+", " ", descripcion.strip())
        return descripcion


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = "__all__"
