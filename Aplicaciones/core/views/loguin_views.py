import traceback # Importa traceback para manejar errores
from django.http import JsonResponse # Importa JsonResponse para enviar respuestas JSON
from django.shortcuts import redirect, render
from django.contrib.auth.models import User # Importa el modelo User de Django
from django.contrib.auth import authenticate,login,logout # Importar funciones para autenticar,logueo y cerrar sesion

# VISTA DE INICIO DE SESION
def index(request):
    return render(request, 'loguin/Index.html')

# METODO PARA INICIAR SESION
def iniciar_sesion(request):
    if(request.user.is_authenticated): # Si el usuario ya está autenticado, redirigir a la página de inicio
        return render(request, 'pages/Page_404.html')
    else:
        if(request.method == 'POST'):
            try:
                identificador = request.POST['identificador'] # Obtiene el usuario o correo
                clave = request.POST['password'] # Obtiene la contraseña
                try:
                    usuario = User.objects.get(
                        username=identificador
                    ) if User.objects.filter(username=identificador).exists() else User.objects.get(email=identificador)
                except User.DoesNotExist:
                    return JsonResponse({ 'error': 'Usuario o correo no encontrado.'}, status=404)
                # Autenticar al usuario
                usuario_autenticado = authenticate(request, username = usuario.username, password=clave)
                if(usuario_autenticado is not None):
                    login(request, usuario_autenticado) # Iniciar sesión del usuario autenticado
                    if(usuario_autenticado.groups.filter(name='Administradores').exists()):
                        return redirect('administrador_index') # Redirigir a la vista principal del administrador
                    elif(usuario_autenticado.groups.filter(name='Docentes').exists()):
                        return redirect('docente_vista') # Redirigir a la vista principal del docente
                    elif(usuario_autenticado.groups.filter(name='Estudiantes').exists()):
                        return redirect('estudiante_vista') # Redirigir a la vista principal del estudiante
                    elif(usuario_autenticado.is_superuser):
                        return redirect('admin:index') # Redirigir a la vista principal del superadministrador
                    else:
                        return JsonResponse({'estado': False, 'mensaje': 'Usuario, email o contraseña incorrectos'}, status=403)
                return JsonResponse({'estado': False, 'mensaje': 'Usuario, email o contraseña incorrectos'}, status=400)
            except Exception as e:
                print(traceback.format_exc())  # Para ver el error en la consola
                return JsonResponse({'estado': False, 'mensaje': 'Ocurrió un error interno, intenta nuevamente'}, status=500)
    return JsonResponse({'mensaje': 'Método no permitido'}, status=405)

# METODO PARA CERRAR SESION
def cerrar_sesion(request):
    logout(request)
    return render(request, 'loguin/Index.html')