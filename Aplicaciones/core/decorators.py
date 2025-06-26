from django.shortcuts import redirect
from functools import wraps
from .models import Docentes, Administradores, Estudiantes

def rol_required(rol):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            usuario = request.user

            # Verificar si el usuario pertenece al rol correcto
            if rol == 'administrador':
                if Administradores.objects.filter(fk_id_persona__fk_id_usuario=usuario).exists():
                    return view_func(request, *args, **kwargs)
                else:
                    return redirect('core_docente') if Docentes.objects.filter(fk_id_persona__fk_id_usuario=usuario).exists() else redirect('core_estudiante')

            elif rol == 'docente':
                if Docentes.objects.filter(fk_id_persona__fk_id_usuario=usuario).exists():
                    return view_func(request, *args, **kwargs)
                else:
                    return redirect('core_admin') if Administradores.objects.filter(fk_id_persona__fk_id_usuario=usuario).exists() else redirect('core_estudiante')

            elif rol == 'estudiante':
                if Estudiantes.objects.filter(fk_id_persona__fk_id_usuario=usuario).exists():
                    return view_func(request, *args, **kwargs)
                else:
                    return redirect('core_admin') if Administradores.objects.filter(fk_id_persona__fk_id_usuario=usuario).exists() else redirect('core_docente')

            else:
                return redirect('inicio')  # Si el rol no es válido, redirigir a inicio

        return wrapper
    return decorator
