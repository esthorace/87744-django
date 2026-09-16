from django.http import HttpResponse
from django.shortcuts import render


def saludar(request):
    return HttpResponse("Hola desde Django")


def saludar2(request):
    mensaje = "Mi App Web"
    print(mensaje)
    return HttpResponse(f"<p>Esta es una prueba de <b>{mensaje}</b></p>")
