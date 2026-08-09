from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import CambioPasswordInicialForm, LoginForm


# ================= FUNCIÓN AUXILIAR DE REDIRECCIÓN =================

def redirigir_por_rol(user):
    """
    Redirige al usuario a su panel correspondiente según sus propiedades de rol.
    Si no posee un rol válido, cierra la sesión para prevenir bucles de redirección.
    """
    if user.es_admin_crm:
        return redirect('PanelAdmin:dashboard')
    elif user.es_panel_user:
        return redirect('PanelUser:home')

    # Fallback de seguridad si el usuario no tiene rol asignado
    return redirect('Base:login')


# ================= VIEWS DE AUTENTICACIÓN =================

def login_view(request):
    """
    Gestiona el inicio de sesión de usuarios.
    Si ya está autenticado, lo redirige a su panel o a cambiar contraseña si es su primer ingreso.
    """
    if request.user.is_authenticated:
        if getattr(request.user, 'debe_cambiar_password', False):
            return redirect('Base:cambiar_password')
        return redirigir_por_rol(request.user)

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            # Redirección obligatoria al cambio de contraseña inicial
            if getattr(user, 'debe_cambiar_password', False):
                return redirect('Base:cambiar_password')

            return redirigir_por_rol(user)
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})


def logout_view(request):
    """
    Cierra la sesión activa del usuario y redirige al inicio de sesión.
    """
    logout(request)
    return redirect('Base:login')


@login_required
def cambiar_password_view(request):
    """
    Obliga al usuario a cambiar su contraseña por primera vez
    si el flag `debe_cambiar_password` está en True.
    """
    if not getattr(request.user, 'debe_cambiar_password', False):
        return redirigir_por_rol(request.user)

    if request.method == 'POST':
        form = CambioPasswordInicialForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            user.debe_cambiar_password = False
            user.save()

            # Mantiene la sesión iniciada tras cambiar la contraseña
            update_session_auth_hash(request, user)
            return redirigir_por_rol(user)
    else:
        form = CambioPasswordInicialForm(user=request.user)

    return render(request, 'cambiar_password.html', {'form': form})