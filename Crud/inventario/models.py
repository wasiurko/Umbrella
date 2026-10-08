from django.conf import settings
from django.db import models


class Perfil(models.Model):
    TIPO_ARQUITECTO = "arquitecto"
    TIPO_TRABAJADOR = "trabajador"
    TIPOS = [
        (TIPO_ARQUITECTO, "Arquitecto"),
        (TIPO_TRABAJADOR, "Trabajador"),
    ]

    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="perfil",
    )
    tipo = models.CharField(max_length=20, choices=TIPOS, default=TIPO_TRABAJADOR)
    cargo = models.CharField(max_length=120)
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["usuario__last_name", "usuario__first_name", "usuario__username"]
        verbose_name = "perfil"
        verbose_name_plural = "perfiles"

    def __str__(self):
        return self.usuario.get_full_name() or self.usuario.username