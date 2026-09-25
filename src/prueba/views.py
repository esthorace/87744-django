from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from prueba.models import Cliente


def saludar(request: HttpRequest) -> HttpResponse:
    return HttpResponse("Hola desde Django")


def saludar_2(request: HttpRequest) -> HttpResponse:
    mensaje = "Mi App Web"
    print(mensaje)
    return HttpResponse(f"<p>Esta es una prueba de <b>{mensaje}</b></p>")


def parametros(request: HttpRequest, nombre: str, apellido: str):
    nombre = nombre.capitalize()
    apellido = apellido.upper()
    return HttpResponse(f"<p><b>{apellido}</b>, {nombre}</p>")


def home(request: HttpRequest) -> HttpResponse:
    from datetime import UTC, datetime

    contexto = {
        "titulo": "Django",
        "año": datetime.now(UTC).year,
    }
    return render(request, "prueba/home.html", contexto)


def notas(request: HttpRequest) -> HttpResponse:
    lista_notas = [1, 10, 4, 7, 8, 5, 7]
    return render(request, "prueba/notas.html", {"notas": lista_notas})


def cliente_list(request: HttpRequest) -> HttpResponse:
    clientes = Cliente.objects.all()
    return render(request, "prueba/cliente_list.html", context={"clientes": clientes})
