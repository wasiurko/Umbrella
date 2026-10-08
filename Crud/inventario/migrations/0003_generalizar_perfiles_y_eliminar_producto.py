from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("inventario", "0002_perfiltrabajador_role_groups"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.DeleteModel(name="Producto"),
        migrations.RenameModel(old_name="PerfilTrabajador", new_name="Perfil"),
        migrations.AddField(
            model_name="perfil",
            name="tipo",
            field=models.CharField(
                choices=[("arquitecto", "Arquitecto"), ("trabajador", "Trabajador")],
                default="trabajador",
                max_length=20,
            ),
        ),
        migrations.AlterField(
            model_name="perfil",
            name="usuario",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="perfil",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterModelOptions(
            name="perfil",
            options={
                "ordering": ["usuario__last_name", "usuario__first_name", "usuario__username"],
                "verbose_name": "perfil",
                "verbose_name_plural": "perfiles",
            },
        ),
    ]