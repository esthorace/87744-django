from django.db import models


class Pais(models.Model):
    nombre = models.CharField()


class Cliente(models.Model):
    nombre = models.CharField()
    apellido = models.CharField()
    pais_origen = models.ForeignKey(Pais, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.apellido.upper()}, {self.nombre.capitalize()}"
