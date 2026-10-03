from django import forms

from .models.categoria import Categoria


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        # fields = ("nombre", "descripcion")
        fields = "__all__"
