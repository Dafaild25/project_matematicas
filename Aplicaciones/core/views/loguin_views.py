import traceback # Importa traceback para manejar errores
from django.http import JsonResponse # Importa JsonResponse para enviar respuestas JSON
from django.shortcuts import redirect, render
from django.contrib.auth.models import User # Importa el modelo User de Django
from django.contrib.auth import authenticate,login,logout # Importar funciones para autenticar,logueo y cerrar sesion
import traceback # Importa traceback para manejar errores
from django.urls import reverse # Importa reverse para generar URLs
from django.db.models import Q # Importa Q para realizar consultas complejas

# VISTA DE INICIO DE SESION
def index(request):
    return render(request, 'loguin/Index.html')

# METODO PARA INICIAR SESION
def iniciar_sesion(request):
    if(request.user.is_authenticated): # Si el usuario ya está autenticado, redirigir a la página de inicio
        # Si ya hay un usuario logueado, cerrar su sesión
        logout(request)
    if request.method != 'POST':
        return JsonResponse({'estado': False, 'mensaje': 'Método no permitido'}, status=405)
    try:
        identificador = request.POST['identificador'].strip() # Obtiene el usuario o correo
        clave = request.POST['password'].strip() # Obtiene la contraseña
        if not identificador or not clave:
            return JsonResponse({'estado': False, 'mensaje': 'Credenciales incompletas'}, status=400)
        try:
            usuario = User.objects.get(Q(username=identificador) | Q(email=identificador))
        except User.DoesNotExist:
            return JsonResponse({'estado': False, 'mensaje': 'Usuario o correo no encontrado.'}, status=404)
        # Autenticar al usuario
        usuario_autenticado = authenticate(request, username = usuario.username, password=clave)
        if(usuario_autenticado is not None):
            login(request, usuario_autenticado) # Iniciar sesión del usuario autenticado
            if usuario_autenticado.groups.filter(name='Administradores').exists():
                url = reverse('core_admin')
            elif usuario_autenticado.groups.filter(name='Docentes').exists():
                url = reverse('core_docente')
            elif usuario_autenticado.groups.filter(name='Estudiantes').exists():
                url = reverse('core_estudiante')
            elif usuario_autenticado.is_superuser:
                url = reverse('admin:index')
            else:
                return JsonResponse({'estado': False, 'mensaje': 'Usuario no tiene permisos asignados'}, status=403)
            return JsonResponse({
                'estado': True,
                'url': url,
                'nombre': f'{usuario_autenticado.first_name} {usuario_autenticado.last_name}'
            })
        return JsonResponse({'estado': False, 'mensaje': 'Usuario, email o contraseña incorrectos'}, status=400)
    except Exception as e:
        print(traceback.format_exc())  # Para ver el error en la consola
        return JsonResponse({'estado': False, 'mensaje': 'Ocurrió un error interno, intenta nuevamente'}, status=500)

# METODO PARA CERRAR SESION
def cerrar_sesion(request):
    logout(request)
    response = redirect('loguin_index')  # Redirigir a la página de inicio de sesión
    response.delete_cookie('sessionid')  # Eliminar la cookie de sesión
    return response  # Retornar la respuesta de redirección