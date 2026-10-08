from .permisos import ADMIN, ARQ, TRABAJADOR


def datos_rol(request):
    usuario = request.user
    if not usuario.is_authenticated:
        return {
            "es_administrador": False,
            "es_gestor_perfiles": False,
            "es_arquitecto": False,
            "es_trabajador": False,
        }
    roles = set(usuario.groups.values_list("name", flat=True))
    return {
        "es_administrador": usuario.is_superuser or ADMIN in roles,
        "es_gestor_perfiles": usuario.is_superuser or ADMIN in roles or ARQ in roles,
        "es_arquitecto": usuario.is_superuser or ARQ in roles,
        "es_trabajador": TRABAJADOR in roles,
    }