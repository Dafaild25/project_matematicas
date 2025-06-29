from django.shortcuts import redirect
from django.urls import resolve, Resolver404
from django.contrib import messages
import logging

logger = logging.getLogger('Aplicaciones.core.views')

class LoginAndNoCacheMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        
        # URLs públicas (no requieren autenticación)
        self.exempt_urls = [
            'loguin_index',       # Vista de login
            'loguin_index_alt',   # Vista de login alternativa (si la tienes)
            'iniciar_sesion',     # Método de iniciar sesión
            'cerrar_sesion',      # Vista de logout
            'admin:login',        # Admin login de Django
            'admin:logout',       # Admin logout de Django
            'admin:index',        # Admin index de Django
            'error_404',          # Página de error 404
        ]
        
        # Mapeo de URLs protegidas y sus roles requeridos
        self.protected_urls = {
            'core_admin': ['Administradores'],
            'obtener_datos_admin': ['Administradores'],
            'core_docente': ['Docentes'],
            'core_estudiante': ['Estudiantes'],
        }

    def __call__(self, request):
        try:
            # Resolver la vista actual por su nombre
            resolved = resolve(request.path_info)
            current_url = resolved.url_name
            
        except Resolver404:
            # Si no se puede resolver la URL, permitir que Django maneje el 404
            logger.warning(f"URL no encontrada: {request.path_info}")
            response = self.get_response(request)
            return self.add_no_cache_headers(response)

        # Debug logging
        logger.debug(f"Usuario: {request.user.username if request.user.is_authenticated else 'Anónimo'} - URL: {current_url}")

        # Verificar autenticación
        if not request.user.is_authenticated:
            if current_url not in self.exempt_urls:
                logger.info(f"Usuario no autenticado redirigido desde: {current_url}")
                return redirect('loguin_index')
        else:
            # Usuario autenticado - verificar permisos para URLs protegidas
            permission_check = self.check_permissions(request, current_url)
            if permission_check:
                return permission_check

        # Continuar con la respuesta
        response = self.get_response(request)
        
        # Agregar encabezados para evitar caché
        return self.add_no_cache_headers(response)

    def check_permissions(self, request, current_url):
        """Verificar si el usuario tiene permisos para la URL actual"""
        
        # Si la URL no está en las protegidas, permitir acceso
        if current_url not in self.protected_urls:
            return None
            
        required_roles = self.protected_urls[current_url]
        user = request.user
        
        # Superuser siempre tiene acceso
        if user.is_superuser:
            logger.debug(f"Superuser {user.username} accediendo a {current_url}")
            return None
        
        # Verificar si el usuario tiene alguno de los roles requeridos
        user_groups = list(user.groups.values_list('name', flat=True))
        has_permission = any(role in user_groups for role in required_roles)
        
        if has_permission:
            logger.debug(f"Usuario {user.username} con grupos {user_groups} accediendo a {current_url}")
            return None
        else:
            logger.warning(f"Usuario {user.username} sin permisos para {current_url}. Grupos: {user_groups}, Requeridos: {required_roles}")
            
            # Verificar si messages está disponible antes de usarlo
            try:
                from django.contrib import messages
                messages.error(request, f'No tienes permisos para acceder a esta página. Roles requeridos: {", ".join(required_roles)}')
            except Exception as e:
                logger.error(f"Error al agregar mensaje: {e}")
            
            return redirect('loguin_index')

    def add_no_cache_headers(self, response):
        """Agregar encabezados para evitar caché"""
        response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        return response