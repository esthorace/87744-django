from django.contrib.auth import authenticate, login
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render


def home(request: HttpRequest) -> HttpResponse:
    return render(request, "core/home.html")


def login_view(request: HttpRequest) -> HttpResponse:
    error = None

    if request.method == "POST":
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")

        # verifica que exista en la tabla de usuarios
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Establece una sesión
            login(request, user)
            return redirect("core:home")

        error = "Usuario o contraseña incorrectos."

    return render(request, "core/login.html", {"error": error})
