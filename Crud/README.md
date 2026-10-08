# Gestión de perfiles

Aplicación MVC con Django 3.2 para crear y administrar perfiles de arquitectos y trabajadores, con inicio de sesión y permisos por rol.

## Funcionalidades

- Crear cuentas y perfiles de arquitectos o trabajadores.
- Buscar y consultar perfiles según el rol.
- Editar perfiles de trabajadores como arquitecto y cualquier perfil como administrador.
- Eliminar perfiles y sus cuentas como administrador.
- Restringir el acceso a rutas protegidas con los grupos de autenticación de Django.

## Roles y permisos

| Rol | Permisos |
| --- | --- |
| Administrador | Ver, crear, editar y eliminar perfiles de arquitectos y trabajadores |
| Arquitecto | Ver perfiles de trabajadores, crear trabajadores y editar sus perfiles |
| Trabajador | Ver únicamente su propio perfil |

## Tecnologías

- Python 3.10
- Django 3.2.25
- SQLite
- HTML y CSS

> Django 3.2 no es compatible oficialmente con Python 3.14. Usa Python 3.10 para este proyecto.

## Instalación

En Windows, desde la carpeta del proyecto:

```powershell
py -3.10 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Abre <http://127.0.0.1:8000/>. El superusuario tiene permisos completos. Los arquitectos se crean desde la pantalla **Perfiles > Crear perfil**; los trabajadores pueden ser creados por el administrador o por un arquitecto.

## Rutas principales

| Ruta | Acción | Acceso |
| --- | --- | --- |
| `/accounts/login/` | Iniciar sesión | Público |
| `/accounts/logout/` | Cerrar sesión | Autenticado |
| `/` | Redirigir según el rol | Autenticado |
| `/perfiles/` | Listar y buscar perfiles | Administrador, Arquitecto |
| `/perfiles/nuevo/` | Crear perfil | Administrador, Arquitecto (solo trabajadores) |
| `/perfiles/<id>/` | Consultar perfil | Administrador, Arquitecto (trabajadores), titular |
| `/perfiles/<id>/editar/` | Editar perfil | Administrador, Arquitecto (solo trabajadores) |
| `/perfiles/<id>/eliminar/` | Eliminar perfil y cuenta | Administrador |
| `/mi-perfil/` | Consultar perfil propio | Trabajador |

## Estructura

- `configuracion/`: ajustes y rutas principales de Django.
- `inventario/`: perfiles, formularios, vistas, permisos y pruebas.
- `templates/`: pantallas HTML.
- `static/`: estilos CSS.
- `manage.py`: comandos para ejecutar y administrar el proyecto.

## Pruebas

```powershell
python manage.py test
```

La ficha conserva únicamente tipo y cargo además de los campos automáticos. La contraseña no tiene reglas mínimas de longitud o complejidad, pero Django sigue guardándola con PBKDF2 por defecto y nunca en texto plano. Solo el administrador ve y puede cambiar nombres de usuario, y puede asignar una nueva contraseña desde la edición. No es posible visualizar la contraseña actual; los demás roles no tienen esos controles.

## Despliegue

La configuración incluida es para desarrollo local. Antes de publicar, configura `SECRET_KEY` mediante una variable de entorno, desactiva `DEBUG` y define `ALLOWED_HOSTS`. No publiques contraseñas de demostración.