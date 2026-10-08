from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import EditarPerfilForm, PerfilForm, UsuarioForm
from .models import Perfil
from .permisos import ADMIN, ARQ, TRABAJADOR, requiere_rol, tiene_rol


@login_required
def inicio(request):
    if tiene_rol(request.user, ADMIN) or tiene_rol(request.user, ARQ):
        return redirect("perfiles:lista")
    if tiene_rol(request.user, TRABAJADOR):
        return redirect("perfiles:mi_perfil")
    raise PermissionDenied


@requiere_rol(ADMIN, ARQ)
def lista_perfiles(request):
    consulta = request.GET.get("q", "").strip()
    perfiles = Perfil.objects.select_related("usuario")
    if not tiene_rol(request.user, ADMIN):
        perfiles = perfiles.filter(tipo=Perfil.TIPO_TRABAJADOR)
    if consulta:
        perfiles = perfiles.filter(
            Q(usuario__first_name__icontains=consulta)
            | Q(usuario__last_name__icontains=consulta)
            | Q(usuario__username__icontains=consulta)
            | Q(cargo__icontains=consulta)
            | Q(tipo__icontains=consulta)
        )
    return render(request, "perfiles/lista.html", {"perfiles": perfiles, "consulta": consulta})


@login_required
def detalle_perfil(request, pk):
    perfil = get_object_or_404(Perfil.objects.select_related("usuario"), pk=pk)
    es_admin = tiene_rol(request.user, ADMIN)
    es_arq = tiene_rol(request.user, ARQ)
    es_trabajador = tiene_rol(request.user, TRABAJADOR)
    puede_ver = es_admin or (
        es_arq and perfil.tipo == Perfil.TIPO_TRABAJADOR
    ) or (
        es_trabajador
        and perfil.tipo == Perfil.TIPO_TRABAJADOR
        and perfil.usuario_id == request.user.id
    )
    if not puede_ver:
        raise PermissionDenied
    return render(request, "perfiles/detalle.html", {"perfil": perfil})


@login_required
def mi_perfil(request):
    if not tiene_rol(request.user, TRABAJADOR):
        raise PermissionDenied
    perfil = get_object_or_404(
        Perfil.objects.select_related("usuario"),
        usuario=request.user,
        tipo=Perfil.TIPO_TRABAJADOR,
    )
    return render(request, "perfiles/detalle.html", {"perfil": perfil})


@requiere_rol(ADMIN, ARQ)
def crear_perfil(request):
    permitir_arq = tiene_rol(request.user, ADMIN)
    usuario_form = UsuarioForm(request.POST or None, prefix="usuario")
    perfil_form = PerfilForm(
        request.POST or None,
        prefix="perfil",
        permitir_arq=permitir_arq,
    )
    if request.method == "POST" and usuario_form.is_valid() and perfil_form.is_valid():
        usuario = usuario_form.save()
        perfil = perfil_form.save(commit=False)
        perfil.usuario = usuario
        perfil.save()
        rol = ARQ if perfil.tipo == Perfil.TIPO_ARQUITECTO else TRABAJADOR
        grupo, _ = Group.objects.get_or_create(name=rol)
        usuario.groups.set([grupo])
        return redirect("perfiles:lista")
    return render(
        request,
        "perfiles/formulario.html",
        {
            "usuario_form": usuario_form,
            "perfil_form": perfil_form,
            "titulo": "Nuevo perfil",
            "permitir_arq": permitir_arq,
        },
    )


@requiere_rol(ADMIN, ARQ)
def editar_perfil(request, pk):
    perfil = get_object_or_404(Perfil.objects.select_related("usuario"), pk=pk)
    es_admin = tiene_rol(request.user, ADMIN)
    if not es_admin and perfil.tipo != Perfil.TIPO_TRABAJADOR:
        raise PermissionDenied
    form = EditarPerfilForm(
        request.POST or None,
        instance=perfil,
        permitir_tipo=es_admin,
        permitir_credenciales=es_admin,
    )
    if request.method == "POST" and form.is_valid():
        form.save()
        if es_admin:
            rol = ARQ if perfil.tipo == Perfil.TIPO_ARQUITECTO else TRABAJADOR
            grupo, _ = Group.objects.get_or_create(name=rol)
            perfil.usuario.groups.set([grupo])
        return redirect("perfiles:lista")
    return render(request, "perfiles/editar.html", {"form": form, "perfil": perfil})


@requiere_rol(ADMIN)
def eliminar_perfil(request, pk):
    perfil = get_object_or_404(Perfil.objects.select_related("usuario"), pk=pk)
    if request.method == "POST":
        usuario = perfil.usuario
        perfil.delete()
        usuario.delete()
        return redirect("perfiles:lista")
    return render(request, "perfiles/confirmar_eliminacion.html", {"perfil": perfil})