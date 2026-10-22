from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
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
            messages.success(request, "Acceso correcto")
            return redirect("ventas:home")

        error = "Usuario o contraseña incorrectos."

    return render(request, "core/login.html", {"error": error})


def logout_view(request: HttpRequest) -> HttpResponse:
    # El cierre de sesión solo se ejecuta por POST (formulario del navbar).
    if request.method == "POST":
        logout(request)
        messages.success(request, "Sesión cerrada")
        # Redirige para que recargar la página no reenvíe el formulario.
        return redirect("core:logout")

    # Un usuario con sesión activa no debe ver la pantalla de despedida.
    if request.user.is_authenticated:
        return redirect("core:home")

    return render(request, "core/logout.html")
