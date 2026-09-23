from django.db import models

# Create your models here.


class Cliente(models.Model):
    nombre = models.CharField()
    apellido = models.CharField()

    def __str__(self) -> str:
        return f"{self.apellido.upper()}, {self.nombre.capitalize()}"
