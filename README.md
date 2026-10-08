# Umbrella

Sistema web en desarrollo para la gestión administrativa de proyectos de construcción. El repositorio actual presenta una base funcional desarrollada con Django para la administración de perfiles, autenticación y control de acceso por roles, con la intención de ampliarse hacia la gestión de personal, herramientas, costos, pagos y presupuestos.

## Objetivo del proyecto

El proyecto busca apoyar la operación de obras de construcción mediante la centralización de información relacionada con:

- registro de personal y perfiles
- control de asistencia
- inventario de herramientas y equipos
- costos directos e indirectos
- pagos y seguimiento de personal
- elaboración de presupuestos y desglose de obra

## Estado actual

Actualmente, el sistema cuenta con una base funcional para gestión de usuarios y perfiles. Se ha implementado la autenticación del sistema, la gestión de usuarios por roles y el CRUD de perfiles.

### Funcionalidades que sí están operando

- autenticación de usuarios
- login y logout
- gestión de perfiles de arquitectos y trabajadores
- permisos por tipo de usuario
- edición y eliminación de perfiles con restricciones por rol
- validación de formularios y pruebas básicas

### Funcionalidades pendientes

- registro de proyectos de construcción
- control de asistencia
- gestión de pagos y nómina
- control de herramientas e inventario
- registro de costos y gastos
- generación de presupuestos y APU
- reportes y análisis de obra

## Alcance previsto

El proyecto se encuentra en una etapa inicial. El alcance actual corresponde a la base del sistema; el alcance futuro contempla la expansión a un módulo completo de administración de obra, con énfasis en control operativo, presupuestación y costos.

### Fases previstas

- Fase 1: autenticación, perfiles y permisos
- Fase 2: proyectos, asistencia y gestión de personal
- Fase 3: inventario, costos y pagos
- Fase 4: presupuestos, APU, reportes y análisis

## Requisitos

- Python 3.10
- Django 3.2.25
- SQLite para entorno de desarrollo
- pip

## Instalación

1. Clonar el repositorio:

```bash
git clone https://github.com/wasiurko/Umbrella.git
cd Umbrella/Crud
```

2. Crear un entorno virtual:

```bash
python3.10 -m venv .venv
source .venv/bin/activate
```

3. Instalar dependencias:

```bash
python -m pip install -r requirements.txt
```

4. Ejecutar migraciones:

```bash
python manage.py migrate
```

5. Ingrese un usuario administrador:
user: adm
password: 123

user: arq
password: 123

user: sano
password: 123

user: pato
password: 123

7. Iniciar la aplicación:

```bash
python manage.py runserver
```

La aplicación quedará disponible en http://127.0.0.1:8000/

## Estructura del proyecto

```text
Umbrella/
├── Crud/
│   ├── configuracion/
│   ├── inventario/
│   ├── templates/
│   ├── static/
│   ├── manage.py
│   ├── requirements.txt
│   └── db.sqlite3
├── README.md
└── ...
```

## Tecnologías utilizadas

- Python
- Django
- SQLite (integrado en VSCode)
- HTML y CSS

## Observaciones

- El proyecto se encuentra en desarrollo.
- La configuración actual está orientada a un entorno local.
- Para producción, se recomienda revisar la configuración de seguridad, variables de entorno y base de datos.
- Debido a la versión de Django, es recomendable utilizar Python 3.10.

## Autor

Jesus Guaygua
