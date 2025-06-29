# Aplicaciones/core/decorators.py

from functools import wraps
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import redirect
from django.contrib import messages
import logging

logger = logging.getLogger('Aplicaciones.core.views')

# ===== FUNCIONES DE VERIFICACIÓN =====
def es_administrador(user):
    """Verificar si el usuario es administrador"""
    return user.is_authenticated and (
        user.is_superuser or 
        user.groups.filter(name='Administradores').exists()
    )

def es_docente(user):
    """Verificar si el usuario es docente"""
    return user.is_authenticated and user.groups.filter(name='Docentes').exists()

def es_estudiante(user):
    """Verificar si el usuario es estudiante"""
    return user.is_authenticated and user.groups.filter(name='Estudiantes').exists()

def es_docente_o_admin(user):
    """Verificar si el usuario es docente o administrador"""
    return user.is_authenticated and (
        user.is_superuser or
        user.groups.filter(name__in=['Administradores', 'Docentes']).exists()
    )

# ===== DECORADORES ESPECÍFICOS =====

def admin_required(view_func):
    """Decorador para vistas que requieren rol de Administrador"""
    @wraps(view_func)
    @login_required(login_url='loguin_index')
    @user_passes_test(es_administrador, login_url='loguin_index')
    def _wrapped_view(request, *args, **kwargs):
        logger.debug(f"Admin acceso: {request.user.username} a {view_func.__name__}")
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def docente_required(view_func):
    """Decorador para vistas que requieren rol de Docente"""
    @wraps(view_func)
    @login_required(login_url='loguin_index')
    @user_passes_test(es_docente, login_url='loguin_index')
    def _wrapped_view(request, *args, **kwargs):
        logger.debug(f"Docente acceso: {request.user.username} a {view_func.__name__}")
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def estudiante_required(view_func):
    """Decorador para vistas que requieren rol de Estudiante"""
    @wraps(view_func)
    @login_required(login_url='loguin_index')
    @user_passes_test(es_estudiante, login_url='loguin_index')
    def _wrapped_view(request, *args, **kwargs):
        logger.debug(f"Estudiante acceso: {request.user.username} a {view_func.__name__}")
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def docente_o_admin_required(view_func):
    """Decorador para vistas que requieren rol de Docente o Administrador"""
    @wraps(view_func)
    @login_required(login_url='loguin_index')
    @user_passes_test(es_docente_o_admin, login_url='loguin_index')
    def _wrapped_view(request, *args, **kwargs):
        logger.debug(f"Docente/Admin acceso: {request.user.username} a {view_func.__name__}")
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def role_required(allowed_roles):
    """
    Decorador genérico para múltiples roles
    Uso: @role_required(['Administradores', 'Docentes'])
    """
    def decorator(view_func):
        @wraps(view_func)
        @login_required(login_url='loguin_index')
        def _wrapped_view(request, *args, **kwargs):
            user = request.user
            
            # Verificar si es superuser
            if user.is_superuser:
                logger.debug(f"Superuser acceso: {user.username} a {view_func.__name__}")
                return view_func(request, *args, **kwargs)
            
            # Verificar si tiene alguno de los roles permitidos
            user_groups = user.groups.values_list('name', flat=True)
            if any(role in user_groups for role in allowed_roles):
                logger.debug(f"Usuario {user.username} con rol válido accedió a {view_func.__name__}")
                return view_func(request, *args, **kwargs)
            
            # Si no tiene permisos
            logger.warning(f"Usuario {user.username} sin permisos para {view_func.__name__}")
            return redirect('loguin_index')
        
        return _wrapped_view
    return decorator

# ===== DECORADOR PARA AJAX =====
def ajax_required(view_func):
    """Decorador para vistas que solo deben responder a peticiones AJAX"""
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            logger.warning(f"Acceso no-AJAX bloqueado a {view_func.__name__}")
            return redirect('loguin_index')
        return view_func(request, *args, **kwargs)
    return _wrapped_view