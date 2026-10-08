from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from .models import Perfil


class UsuarioForm(UserCreationForm):
    first_name = forms.CharField(label="Nombre", max_length=150)
    last_name = forms.CharField(label="Apellidos", max_length=150)

    class Meta:
        model = get_user_model()
        fields = ("username", "first_name", "last_name")


class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ["tipo", "cargo"]
        labels = {"tipo": "Tipo de perfil", "cargo": "Cargo o especialidad"}

    def __init__(self, *args, permitir_arq=True, **kwargs):
        super().__init__(*args, **kwargs)
        if not permitir_arq:
            self.fields.pop("tipo")


class EditarPerfilForm(forms.ModelForm):
    campo_usuario = get_user_model()._meta.get_field("username")
    username = forms.CharField(
        label="Usuario",
        max_length=campo_usuario.max_length,
        validators=campo_usuario.validators,
    )
    nombre = forms.CharField(label="Nombre", max_length=150)
    apellidos = forms.CharField(label="Apellidos", max_length=150)
    nueva_contrasena = forms.CharField(
        label="Nueva contraseña (opcional)",
        required=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text="Déjala vacía para conservarla. La contraseña actual no se puede ver.",
    )

    class Meta:
        model = Perfil
        fields = [
            "username",
            "nombre",
            "apellidos",
            "tipo",
            "cargo",
            "nueva_contrasena",
        ]
        labels = {"tipo": "Tipo de perfil", "cargo": "Cargo o especialidad"}

    def __init__(self, *args, permitir_tipo=True, permitir_credenciales=False, **kwargs):
        super().__init__(*args, **kwargs)
        if not permitir_tipo:
            self.fields.pop("tipo")
        if not permitir_credenciales:
            self.fields.pop("username")
            self.fields.pop("nueva_contrasena")
        usuario = self.instance.usuario
        if permitir_credenciales:
            self.fields["username"].initial = usuario.username
        self.fields["nombre"].initial = usuario.first_name
        self.fields["apellidos"].initial = usuario.last_name

    def clean_username(self):
        username = self.cleaned_data["username"]
        usuarios = get_user_model()._default_manager.filter(username__iexact=username)
        if usuarios.exclude(pk=self.instance.usuario_id).exists():
            raise forms.ValidationError("Ese nombre de usuario ya está en uso.")
        return username

    def save(self, commit=True):
        perfil = super().save(commit=False)
        perfil.usuario.username = self.cleaned_data.get("username", perfil.usuario.username)
        perfil.usuario.first_name = self.cleaned_data["nombre"]
        perfil.usuario.last_name = self.cleaned_data["apellidos"]
        nueva_contrasena = self.cleaned_data.get("nueva_contrasena")
        if nueva_contrasena:
            perfil.usuario.set_password(nueva_contrasena)
        if commit:
            perfil.usuario.save()
            perfil.save()
        return perfil