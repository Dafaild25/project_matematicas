import traceback
import logging
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.db.models import Q

# Configurar logging - usa el logger específico de tu app
logger = logging.getLogger('Aplicaciones.core.views')

# FUNCIÓN AUXILIAR PARA OBTENER URL DE REDIRECCIÓN SEGÚN EL ROL
def get_redirect_url_by_role(user):
    """Retorna la URL de redirección según el rol del usuario"""
    if user.is_superuser:
        return 'admin:index'
    elif user.groups.filter(name='Administradores').exists():
        return 'core_admin'
    elif user.groups.filter(name='Docentes').exists():
        return 'core_docente'
    elif user.groups.filter(name='Estudiantes').exists():
        return 'core_estudiante'
    else:
        return None  # Usuario sin rol asignado

# FUNCIÓN AUXILIAR PARA REDIRIGIR SEGÚN EL ROL
def redirect_by_role(user, request):
    """Redirige al usuario según su rol/grupo"""
    redirect_url = get_redirect_url_by_role(user)
    
    if redirect_url:
        return redirect(redirect_url)
    else:
        # Usuario sin rol asignado
        logout(request)
        messages.error(request, 'Tu cuenta no tiene permisos asignados. Contacta al administrador.')
        logger.warning(f"Usuario sin rol asignado deslogueado: {user.username}")
        return redirect('loguin_index')

# VISTA DE INICIO DE SESION
def index(request):
    # Si el usuario ya está autenticado, redirigir según su rol
    if request.user.is_authenticated:
        return redirect_by_role(request.user, request)
    return render(request, 'loguin/Index.html')

# METODO PARA INICIAR SESION
@csrf_protect
@require_http_methods(["GET", "POST"])
def iniciar_sesion(request):
    # Si el usuario ya está autenticado, redirigir
    if request.user.is_authenticated:
        return redirect_by_role(request.user, request)
    
    if request.method == 'GET':
        return render(request, 'loguin/Index.html')
    
    # Método POST
    try:
        identificador = request.POST.get('identificador', '').strip()
        clave = request.POST.get('password', '').strip()
        
        # Validar que los campos no estén vacíos
        if not identificador or not clave:
            error_msg = 'Usuario/email y contraseña son requeridos'
            # ← CAMBIO 1: Verificar si es AJAX o formulario normal
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'estado': False, 'mensaje': error_msg}, status=400)
            else:
                messages.error(request, error_msg)
                return render(request, 'loguin/Index.html')
        
        # Buscar usuario por username o email
        usuario = None
        try:
            # Usar Q objects para una búsqueda más eficiente
            usuario = User.objects.get(
                Q(username=identificador) | Q(email=identificador)
            )
        except User.DoesNotExist:
            logger.warning(f"Intento de login fallido: usuario/email '{identificador}' no encontrado")
            error_msg = 'Usuario, email o contraseña incorrectos'
            # ← CAMBIO 2: Manejar formulario normal
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'estado': False, 'mensaje': error_msg}, status=401)
            else:
                messages.error(request, error_msg)
                return render(request, 'loguin/Index.html')
        except User.MultipleObjectsReturned:
            # En caso de duplicados (no debería pasar, pero por seguridad)
            logger.error(f"Múltiples usuarios encontrados para '{identificador}'")
            error_msg = 'Error en la configuración de usuarios'
            # ← CAMBIO 3: Manejar formulario normal
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'estado': False, 'mensaje': error_msg}, status=500)
            else:
                messages.error(request, error_msg)
                return render(request, 'loguin/Index.html')
        
        # Verificar si el usuario está activo
        if not usuario.is_active:
            logger.warning(f"Intento de login con usuario inactivo: {usuario.username}")
            error_msg = 'Esta cuenta está desactivada'
            # ← CAMBIO 4: Manejar formulario normal
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'estado': False, 'mensaje': error_msg}, status=401)
            else:
                messages.error(request, error_msg)
                return render(request, 'loguin/Index.html')
        
        # Autenticar al usuario
        usuario_autenticado = authenticate(request, username=usuario.username, password=clave)
        
        if usuario_autenticado is not None:
            # Verificar que el usuario tenga un rol asignado ANTES de hacer login
            redirect_url_name = get_redirect_url_by_role(usuario_autenticado)
            
            if not redirect_url_name:
                # Usuario sin rol - no permitir login
                logger.warning(f"Intento de login de usuario sin rol: {usuario_autenticado.username}")
                error_msg = 'Tu cuenta no tiene permisos asignados. Contacta al administrador.'
                # ← CAMBIO 5: Manejar formulario normal
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({'estado': False, 'mensaje': error_msg}, status=403)
                else:
                    messages.error(request, error_msg)
                    return render(request, 'loguin/Index.html')
            
            # Login exitoso
            login(request, usuario_autenticado)
            logger.info(f"Login exitoso para usuario: {usuario_autenticado.username}")
            
            # Para peticiones AJAX, devolver JSON con la URL de redirección
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'estado': True, 
                    'mensaje': 'Login exitoso',
                    'redirect_url': redirect_url_name
                })
            else:
                # Para peticiones normales, redirigir directamente
                return redirect(redirect_url_name)
        else:
            # Credenciales incorrectas
            logger.warning(f"Credenciales incorrectas para usuario: {identificador}")
            error_msg = 'Usuario o contraseña incorrectos'
            # ← CAMBIO 6: Manejar formulario normal
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'estado': False, 'mensaje': error_msg}, status=401)
            else:
                messages.error(request, error_msg)
                return render(request, 'loguin/Index.html')
            
    except Exception as e:
        logger.error(f"Error en iniciar_sesion: {str(e)}\n{traceback.format_exc()}")
        error_msg = 'Ocurrió un error interno, intenta nuevamente'
        # ← CAMBIO 7: Manejar formulario normal
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'estado': False, 'mensaje': error_msg}, status=500)
        else:
            messages.error(request, error_msg)
            return render(request, 'loguin/Index.html')

# METODO PARA CERRAR SESION
@login_required
def cerrar_sesion(request):
    """Cerrar sesión del usuario"""
    username = request.user.username if request.user.is_authenticated else "Usuario desconocido"
    logout(request)
    logger.info(f"Logout exitoso para usuario: {username}")
    
    # Limpiar mensajes de sesión
    if hasattr(request, '_messages'):
        list(messages.get_messages(request))
    
    response = redirect('loguin_index')
    
    # Asegurar que las cookies se eliminen
    response.delete_cookie('sessionid')
    response.delete_cookie('csrftoken')
    
    return response

# VISTA PARA MANEJAR ERRORES 404 (opcional)
def error_404(request):
    return render(request, 'pages/Page_404.html', status=404)