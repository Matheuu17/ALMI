from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from Base.models import Usuario
from .forms import CrearUsuarioForm, EditarUsuarioForm


@login_required
def dashboard_view(request):
    """
    Panel de administración para la gestión centralizada de usuarios.
    Permite listar, registrar nuevos usuarios o cargar el formulario de edición.
    """
    if not request.user.es_admin_crm:
        messages.error(request, 'No tienes permisos de administración.')
        return redirect('PanelUser:home')

    # Detectar si se está solicitando editar un usuario específico por GET o POST
    usuario_id = request.GET.get('editar') or request.POST.get('usuario_id')
    usuario_a_editar = get_object_or_404(Usuario, id=usuario_id) if usuario_id else None

    if request.method == 'POST':
        if usuario_a_editar:
            form = EditarUsuarioForm(request.POST, instance=usuario_a_editar)
            if form.is_valid():
                form.save()
                messages.success(request, f'Usuario {usuario_a_editar.nombre_completo} actualizado correctamente.')
                return redirect('PanelAdmin:dashboard')
        else:
            form = CrearUsuarioForm(request.POST)
            if form.is_valid():
                usuario = form.save()
                messages.success(request, f'Usuario {usuario.nombre_completo} registrado con éxito.')
                return redirect('PanelAdmin:dashboard')
    else:
        if usuario_a_editar:
            form = EditarUsuarioForm(instance=usuario_a_editar)
        else:
            form = CrearUsuarioForm()

    usuarios = Usuario.objects.all().order_by('-creado_en')

    return render(request, 'dashboard.html', {
        'form': form,
        'usuarios': usuarios,
        'usuario_a_editar': usuario_a_editar,
    })


@login_required
@require_POST
def toggle_estado_usuario_view(request, user_id):
    """
    Alterna el estado activo/desactivado de la cuenta de un usuario.
    Requiere método POST por seguridad.
    """
    if not request.user.es_admin_crm:
        return redirect('PanelUser:home')

    usuario = get_object_or_404(Usuario, id=user_id)
    if usuario == request.user:
        messages.error(request, 'No puedes desactivar tu propio usuario.')
    else:
        usuario.is_active = not usuario.is_active
        usuario.save()
        estado = "activado" if usuario.is_active else "desactivado"
        messages.info(request, f'Usuario {usuario.nombre_completo} {estado}.')

    return redirect('PanelAdmin:dashboard')


@login_required
@require_POST
def reset_password_usuario_view(request, user_id):
    """
    Restablece la contraseña de un usuario a su DNI y marca la bandera
    `debe_cambiar_password` en True para exigir el cambio en el próximo login.
    """
    if not request.user.es_admin_crm:
        return redirect('PanelUser:home')

    usuario = get_object_or_404(Usuario, id=user_id)
    usuario.set_password(usuario.dni)
    usuario.debe_cambiar_password = True
    usuario.save()
    messages.success(request, f'Contraseña de {usuario.nombre_completo} restablecida a su DNI ({usuario.dni}).')

    return redirect('PanelAdmin:dashboard')