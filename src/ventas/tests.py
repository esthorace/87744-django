from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Proveedor, Vendedor

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


class VendedorDetailFotoTest(TestCase):
    """La foto de perfil se muestra dentro del detalle, no como enlace externo."""

    @classmethod
    def setUpTestData(cls):
        cls.staff = User.objects.create_user(
            "staff", password="x", is_staff=True, first_name="Ana"
        )

    def setUp(self):
        self.client.force_login(self.staff)

    def test_muestra_imagen_en_el_head(self):
        vendedor = Vendedor.objects.create(
            usuario=self.staff,
            foto_perfil="vendedores/perfiles/foto.png",
        )

        response = self.client.get(
            reverse("ventas:vendedor_detail", args=[vendedor.pk])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response, '<img src="/media/vendedores/perfiles/foto.png"'
        )
        self.assertContains(response, "Foto de perfil de Ana")
        self.assertNotContains(response, "Ver imagen")
        self.assertNotContains(response, 'target="_blank"')

    def test_sin_foto_muestra_icono_neutro(self):
        vendedor = Vendedor.objects.create(usuario=self.staff)

        response = self.client.get(
            reverse("ventas:vendedor_detail", args=[vendedor.pk])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "detail-avatar-fallback")
        self.assertContains(response, "👤")
        self.assertNotContains(response, "<img")


class ProveedorCrudTest(TestCase):
    """CRUD de Proveedores, incluida la validación de contacto del modelo."""

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user("staff", password="x", is_staff=True)
        cls.normal = User.objects.create_user("normal", password="x")
        cls.proveedor = Proveedor.objects.create(
            nombre="Distribuidora Norte",
            telefono="123456",
            email="norte@example.com",
        )

    def setUp(self):
        self.client.force_login(self.user)

    def test_usuario_sin_staff_puede_ver_pero_no_modificar(self):
        self.client.force_login(self.normal)

        self.assertEqual(
            self.client.get(reverse("ventas:proveedor_list")).status_code, 200
        )
        self.assertEqual(
            self.client.get(
                reverse("ventas:proveedor_detail", args=[self.proveedor.pk])
            ).status_code,
            200,
        )

        urls = (
            reverse("ventas:proveedor_create"),
            reverse("ventas:proveedor_update", args=[self.proveedor.pk]),
            reverse("ventas:proveedor_delete", args=[self.proveedor.pk]),
        )
        for url in urls:
            with self.subTest(url=url):
                self.assertEqual(self.client.get(url).status_code, 403)
                self.assertEqual(self.client.post(url, {}).status_code, 403)

    def test_listado_oculta_acciones_de_escritura_a_no_staff(self):
        self.client.force_login(self.normal)

        response = self.client.get(reverse("ventas:proveedor_list"))

        self.assertContains(
            response,
            reverse("ventas:proveedor_detail", args=[self.proveedor.pk]),
        )
        self.assertNotContains(response, reverse("ventas:proveedor_create"))
        self.assertNotContains(
            response,
            reverse("ventas:proveedor_update", args=[self.proveedor.pk]),
        )
        self.assertNotContains(
            response,
            reverse("ventas:proveedor_delete", args=[self.proveedor.pk]),
        )

    def test_listado_muestra_acciones_de_escritura_a_staff(self):
        response = self.client.get(reverse("ventas:proveedor_list"))

        self.assertContains(response, reverse("ventas:proveedor_create"))
        self.assertContains(
            response,
            reverse("ventas:proveedor_update", args=[self.proveedor.pk]),
        )
        self.assertContains(
            response,
            reverse("ventas:proveedor_delete", args=[self.proveedor.pk]),
        )

    def test_listado_y_busqueda(self):
        response = self.client.get(reverse("ventas:proveedor_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "ventas/proveedor_list.html")
        self.assertContains(response, "Distribuidora Norte")

        for termino in ("Distribuidora", "123456", "norte@example.com"):
            with self.subTest(termino=termino):
                response = self.client.get(
                    reverse("ventas:proveedor_list"), {"busqueda": termino}
                )
                self.assertContains(response, "Distribuidora Norte")

    def test_detail(self):
        response = self.client.get(
            reverse("ventas:proveedor_detail", args=[self.proveedor.pk])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "norte@example.com")

    def test_create_valido(self):
        response = self.client.post(
            reverse("ventas:proveedor_create"),
            {"nombre": "Distribuidora Sur", "telefono": "555", "email": ""},
        )
        self.assertRedirects(response, reverse("ventas:proveedor_list"))
        self.assertTrue(Proveedor.objects.filter(nombre="Distribuidora Sur").exists())

    def test_create_sin_contacto_es_invalido(self):
        response = self.client.post(
            reverse("ventas:proveedor_create"),
            {"nombre": "Sin contacto", "telefono": "", "email": ""},
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Proveedor.objects.filter(nombre="Sin contacto").exists())
        self.assertContains(
            response,
            "Debe proporcionar al menos un medio de contacto",
            count=2,
        )

    def test_update(self):
        response = self.client.post(
            reverse("ventas:proveedor_update", args=[self.proveedor.pk]),
            {
                "nombre": "Distribuidora Norte",
                "telefono": "",
                "email": "nuevo@example.com",
            },
        )
        self.assertRedirects(response, reverse("ventas:proveedor_list"))
        self.proveedor.refresh_from_db()
        self.assertEqual(self.proveedor.email, "nuevo@example.com")
        self.assertEqual(self.proveedor.telefono, "")

    def test_delete(self):
        response = self.client.post(
            reverse("ventas:proveedor_delete", args=[self.proveedor.pk])
        )
        self.assertRedirects(response, reverse("ventas:proveedor_list"))
        self.assertFalse(Proveedor.objects.exists())
