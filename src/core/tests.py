from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class LoginViewTests(TestCase):
    def test_home_access_link_points_to_login(self):
        response = self.client.get(reverse("core:home"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            f'href="{reverse("core:login")}" class="nav-cta">Acceder</a>',
        )

    def test_successful_login_redirects_to_ventas_home(self):
        user = get_user_model().objects.create_user(
            username="usuario",
            password="clave-de-prueba",
        )

        response = self.client.post(
            reverse("core:login"),
            {"username": user.username, "password": "clave-de-prueba"},
        )

        self.assertRedirects(response, reverse("ventas:home"))
        self.assertEqual(self.client.session["_auth_user_id"], str(user.pk))
