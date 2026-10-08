from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.test import TestCase
from django.urls import reverse

from .models import Perfil
from .permisos import ADMIN, ARQ, TRABAJADOR


class PruebasPerfiles(TestCase):
    def setUp(self):
        User = get_user_model()
        self.admin = User.objects.create_user(username="adm", password="1")
        self.admin.groups.add(Group.objects.get(name=ADMIN))
        self.arquitecto = User.objects.create_user(username="arq", password="1")
        self.arquitecto.groups.add(Group.objects.get(name=ARQ))
        self.trabajador = User.objects.create_user(username="sano", password="1")
        self.trabajador.groups.add(Group.objects.get(name=TRABAJADOR))
        self.perfil = Perfil.objects.create(
            usuario=self.trabajador,
            tipo=Perfil.TIPO_TRABAJADOR,
            cargo="Albañil",
        )

    def test_admin_crea_edita_y_elimina(self):
        self.client.force_login(self.admin)
        response = self.client.post(
            reverse("perfiles:crear"),
            {
                "usuario-username": "nuevo",
                "usuario-first_name": "Nuevo",
                "usuario-last_name": "Trabajador",
                "usuario-password1": "1",
                "usuario-password2": "1",
                "perfil-tipo": "trabajador",
                "perfil-cargo": "Residente",
            },
        )
        self.assertRedirects(response, reverse("perfiles:lista"))
        nuevo = get_user_model().objects.get(username="nuevo")
        self.assertTrue(nuevo.groups.filter(name=TRABAJADOR).exists())
        self.assertNotEqual(nuevo.password, "1")

        response = self.client.post(
            reverse("perfiles:editar", args=[nuevo.perfil.pk]),
            {
                "username": "nuevo_editado",
                "nombre": "Nuevo",
                "apellidos": "Trabajador",
                "tipo": "trabajador",
                "cargo": "Supervisor",
                "nueva_contrasena": "2",
            },
        )
        self.assertRedirects(response, reverse("perfiles:lista"))
        nuevo.refresh_from_db()
        self.assertEqual(nuevo.username, "nuevo_editado")
        self.assertTrue(nuevo.check_password("2"))

        response = self.client.post(reverse("perfiles:eliminar", args=[nuevo.perfil.pk]))
        self.assertRedirects(response, reverse("perfiles:lista"))
        self.assertFalse(get_user_model().objects.filter(pk=nuevo.pk).exists())

    def test_arquitecto_crea_y_edita_solo_trabajadores(self):
        self.client.force_login(self.arquitecto)
        response = self.client.post(
            reverse("perfiles:crear"),
            {
                "usuario-username": "otro",
                "usuario-first_name": "Otro",
                "usuario-last_name": "Trabajador",
                "usuario-password1": "1",
                "usuario-password2": "1",
                "perfil-tipo": "arquitecto",
                "perfil-cargo": "Pintor",
            },
        )
        self.assertRedirects(response, reverse("perfiles:lista"))
        otro = get_user_model().objects.get(username="otro")
        self.assertEqual(otro.perfil.tipo, Perfil.TIPO_TRABAJADOR)

        response = self.client.get(reverse("perfiles:editar", args=[otro.perfil.pk]))
        self.assertNotContains(response, "Nueva contraseña")
        self.assertNotContains(response, otro.username)
        self.assertEqual(
            self.client.post(
                reverse("perfiles:eliminar", args=[otro.perfil.pk])
            ).status_code,
            403,
        )

    def test_trabajador_solo_ve_su_perfil(self):
        self.client.force_login(self.trabajador)
        self.assertEqual(self.client.get(reverse("perfiles:mi_perfil")).status_code, 200)
        self.assertEqual(self.client.get(reverse("perfiles:lista")).status_code, 403)

    def test_lista_requiere_sesion(self):
        response = self.client.get(reverse("perfiles:lista"))
        self.assertRedirects(
            response,
            f"{reverse('login')}?next={reverse('perfiles:lista')}",
        )