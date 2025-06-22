from django.shortcuts import render
from django.shortcuts import get_object_or_404
from ...models import Estudiantes, Matriculas,Modulos,Niveles,User
from django.contrib.auth.decorators import login_required


@login_required
def estudiante_modulo(request):
    estudiante = Estudiantes.objects.get(fk_id_persona__fk_id_usuario=request.user)

    # Traer todas las clases del estudiante
    matriculas = Matriculas.objects.filter(fk_estudiante=estudiante).select_related('fk_clase__fk_modulo')

    # Extraer módulos únicos desde las clases
    modulos = set(matricula.fk_clase.fk_modulo for matricula in matriculas)

    contexto = {
        'modulos': modulos
    }
    return render(request, 'masterestudiante/modulo/Estudiante_Modulo.html', contexto)

@login_required
def ver_niveles_modulo(request, modulo_id):
    estudiante = Estudiantes.objects.get(fk_id_persona__fk_id_usuario=request.user)
    
    modulo = get_object_or_404(Modulos, pk=modulo_id)

    # Filtrar solo niveles del módulo
    niveles = Niveles.objects.filter(fk_modulo=modulo).order_by('orden')

    contexto = {
        'modulo': modulo,
        'niveles': niveles,
        'estudiante': estudiante
    }

    return render(request, 'masterestudiante/nivel/Estudiante_Nivel.html', contexto)