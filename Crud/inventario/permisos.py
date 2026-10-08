from functools import wraps

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied


ADMIN = "Administrador"
ARQ = "Arquitecto/Contratista"
TRABAJADOR = "Trabajador"


def tiene_rol(usuario, rol):
    return usuario.is_superuser or usuario.groups.filter(name=rol).exists()


def requiere_rol(*roles):
    def decorador(vista):
        @login_required
        @wraps(vista)
        def protegida(request, *args, **kwargs):
            if request.user.is_superuser or request.user.groups.filter(name__in=roles).exists():
                return vista(request, *args, **kwargs)
            raise PermissionDenied

        return protegida

    return decorador