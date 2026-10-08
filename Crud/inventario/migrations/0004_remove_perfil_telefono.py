from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [("inventario", "0003_generalizar_perfiles_y_eliminar_producto")]

    operations = [migrations.RemoveField(model_name="perfil", name="telefono")]