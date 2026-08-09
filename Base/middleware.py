from django.shortcuts import redirect
from django.urls import reverse


class CambioPasswordObligatorioMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        usuario = request.user

        if (
            usuario.is_authenticated
            and not usuario.is_superuser
            and getattr(usuario, 'debe_cambiar_password', False)
        ):
            rutas_permitidas = [
                reverse('Base:cambiar_password'),
                reverse('Base:logout'),
            ]

            if request.path not in rutas_permitidas:
                return redirect('Base:cambiar_password')

        return self.get_response(request)


class NoCacheMiddleware:
    """
    Middleware para evitar que las páginas protegidas se guarden en la caché del navegador.
    Si el usuario cierra sesión y le da al botón 'Atrás', el navegador se verá obligado
    a hacer una petición al servidor, el cual lo redirigirá al Login si no hay sesión activa.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Se aplica solo si el usuario está autenticado o en rutas protegidas
        if request.user.is_authenticated or request.path.startswith('/panel_admin'):
            response['Cache-Control'] = 'no-cache, no-store, must-revalidate, max-age=0'
            response['Pragma'] = 'no-cache'
            response['Expires'] = '0'

        return response