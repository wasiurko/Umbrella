from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


ROLE_GROUPS = ["Administrador", "Arquitecto/Contratista", "Trabajador"]


def crear_grupos(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    db = schema_editor.connection.alias
    for nombre in ROLE_GROUPS:
        Group.objects.using(db).get_or_create(name=nombre)


def borrar_grupos(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    db = schema_editor.connection.alias
    Group.objects.using(db).filter(name__in=ROLE_GROUPS).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("inventario", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="PerfilTrabajador",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("cargo", models.CharField(max_length=120)),
                ("telefono", models.CharField(blank=True, max_length=30)),
                ("creado", models.DateTimeField(auto_now_add=True)),
                ("actualizado", models.DateTimeField(auto_now=True)),
                ("usuario", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name="perfil_trabajador", to=settings.AUTH_USER_MODEL)),
            ],
            options={
                "verbose_name": "perfil de trabajador",
                "verbose_name_plural": "perfiles de trabajadores",
                "ordering": ["usuario__last_name", "usuario__first_name", "usuario__username"],
            },
        ),
        migrations.RunPython(crear_grupos, borrar_grupos),
    ]