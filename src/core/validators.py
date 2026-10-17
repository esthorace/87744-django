import re
from typing import Any

from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible


@deconstructible
class ValidarTextoEspañol:
    def __init__(self, min_longitud: int, mensaje: str | None = None):
        self.min_longitud = min_longitud
        self.mensaje = mensaje
        self.patron = r"^[a-zA-záéíóúÁÉÍÓÚüÜñÑ ]+$"

    def __call__(self, valor: str) -> Any:
        texto = valor.strip() if valor else ""

        # Validación de longitud
        if len(texto) < self.min_longitud:
            m = self.mensaje or f"El texto debe contener al menos {self.min_longitud} caracteres."
            raise ValidationError(m)

        # Patron: solo letras en español y espacios sencillos
        if not re.match(self.patron, texto):
            m = (
                self.mensaje
                or "El texto solo puede contener letras, acentos y espacios, sin números ni caracteres especiales."
            )
            raise ValidationError(m)
