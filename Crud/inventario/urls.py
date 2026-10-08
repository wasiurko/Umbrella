from django.urls import path

from . import vistas

app_name = "perfiles"

urlpatterns = [
    path("", vistas.inicio, name="inicio"),
    path("perfiles/", vistas.lista_perfiles, name="lista"),
    path("perfiles/nuevo/", vistas.crear_perfil, name="crear"),
    path("perfiles/<int:pk>/", vistas.detalle_perfil, name="detalle"),
    path("perfiles/<int:pk>/editar/", vistas.editar_perfil, name="editar"),
    path("perfiles/<int:pk>/eliminar/", vistas.eliminar_perfil, name="eliminar"),
    path("mi-perfil/", vistas.mi_perfil, name="mi_perfil"),
]