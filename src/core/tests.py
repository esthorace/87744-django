from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from django.urls import reverse


class LoginViewTests(TestCase):
    def test_home_access_link_points_to_login(self):
        response = self.client.get(reverse("core:home"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            f'href="{reverse("core:login")}" class="nav-cta">Acceder</a>',
        )

    def test_authenticated_user_sees_panel_link(self):
        user = get_user_model().objects.create_user(
            username="usuario",
            password="clave-de-prueba",
        )
        self.client.force_login(user)

        response = self.client.get(reverse("core:home"))

        self.assertContains(
            response,
            f'href="{reverse("ventas:home")}" class="nav-cta">Ventas</a>',
        )
        self.assertNotContains(response, "Acceder")

    def test_successful_login_redirects_to_ventas_home(self):
        user = get_user_model().objects.create_user(
            username="usuario",
            password="clave-de-prueba",
        )

        response = self.client.post(
            reverse("core:login"),
            {"username": user.username, "password": "clave-de-prueba"},
            follow=True,
        )

        self.assertRedirects(response, reverse("ventas:home"))
        self.assertEqual(self.client.session["_auth_user_id"], str(user.pk))
        self.assertContains(response, f"Acceso correcto. ¡Bienvenido {user.username}!")


class LogoutViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="usuario",
            password="clave-de-prueba",
        )
        self.client.force_login(self.user)

    def test_post_closes_session_and_redirects_to_confirmation(self):
        response = self.client.post(reverse("core:logout"))

        self.assertRedirects(response, reverse("core:logout"))
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_post_shows_success_message(self):
        response = self.client.post(reverse("core:logout"), follow=True)

        self.assertContains(response, "Sesión cerrada")

    def test_get_does_not_log_out_authenticated_user(self):
        response = self.client.get(reverse("core:logout"))

        self.assertRedirects(response, reverse("core:home"))
        self.assertIn("_auth_user_id", self.client.session)

    def test_get_for_anonymous_user_shows_confirmation(self):
        self.client.logout()

        response = self.client.get(reverse("core:logout"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sesión cerrada")


class ErrorPagesTests(TestCase):
    """Las páginas de error usan templates propios con el estilo del sitio."""

    def test_403_usa_template_propio(self):
        user = get_user_model().objects.create_user(
            username="sin-staff",
            password="clave-de-prueba",
        )
        self.client.force_login(user)

        response = self.client.get(reverse("ventas:vendedor_list"))

        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, "403.html")
        self.assertContains(response, "Acceso restringido", status_code=403)
        self.assertContains(response, "core/css/error.css", status_code=403)

    @override_settings(DEBUG=False)
    def test_404_usa_template_propio(self):
        user = get_user_model().objects.create_user(
            username="staff",
            password="clave-de-prueba",
            is_staff=True,
        )
        self.client.force_login(user)

        response = self.client.get("/ruta-que-no-existe/")

        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, "404.html")
        self.assertContains(response, "Página no encontrada", status_code=404)
        self.assertContains(response, "core/css/error.css", status_code=404)
