from django.shortcuts import redirect
from django.urls import resolve

class LoginAndNoCacheMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.exempt_urls = [
            'loguin_index',       # Vista de login
            'iniciar_sesion',    # Metodo de iniciar sesión
            'cerrar_sesion',      # Vista de logout
            'admin:login',
            'admin:logout',
            'admin:index',
            # Agrega más nombres de URL públicas si las tienes
        ]

    def __call__(self, request):
        # Resolver la vista actual por su nombre
        current_url = resolve(request.path_info).url_name

        # Permitir acceso si el usuario está autenticado o si es una URL exenta
        if not request.user.is_authenticated and current_url not in self.exempt_urls:
            return redirect('loguin_index')

        # Continuar con la respuesta
        response = self.get_response(request)

        # Agregar encabezados para evitar caché
        response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'

        return response
