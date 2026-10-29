from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Vendedor

VENDEDOR_URLS = (
    "vendedor_list",
    "vendedor_create",
)


class StaffAccessTest(TestCase):
    """Solo los miembros del staff pueden usar las vistas de Vendedores."""

    @classmethod
    def setUpTestData(cls):
        cls.staff = User.objects.create_user("staff", password="x", is_staff=True)
        cls.normal = User.objects.create_user("normal", password="x")
        cls.vendedor = Vendedor.objects.create(usuario=cls.normal)

    def urls_con_pk(self):
        return (
            reverse("ventas:vendedor_list"),
            reverse("ventas:vendedor_create"),
            reverse("ventas:vendedor_detail", args=[self.vendedor.pk]),
            reverse("ventas:vendedor_update", args=[self.vendedor.pk]),
            reverse("ventas:vendedor_delete", args=[self.vendedor.pk]),
        )

    def test_anonimo_redirige_al_login(self):
        for name in VENDEDOR_URLS:
            with self.subTest(name=name):
                response = self.client.get(reverse(f"ventas:{name}"))
                self.assertEqual(response.status_code, 302)
                self.assertIn(reverse("core:login"), response.url)

    def test_usuario_sin_staff_recibe_403(self):
        self.client.force_login(self.normal)
        for url in self.urls_con_pk():
            with self.subTest(url=url):
                self.assertEqual(self.client.get(url).status_code, 403)
                self.assertEqual(self.client.post(url, {}).status_code, 403)

    def test_staff_accede(self):
        self.client.force_login(self.staff)
        for url in self.urls_con_pk():
            with self.subTest(url=url):
                self.assertEqual(self.client.get(url).status_code, 200)
