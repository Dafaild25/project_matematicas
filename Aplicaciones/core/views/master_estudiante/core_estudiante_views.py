from django.shortcuts import render
from django.contrib.auth.models import User # Importar modelo User de Django
from ...models import *
from Aplicaciones.core.decorators import rol_required # Importar decorador para requerir estudiante

# Create your views here.
@rol_required('estudiante')
def core_estudiante(request):
    estudiante = Estudiantes.objects.get(fk_id_persona__fk_id_usuario=request.user)

    # Clases donde está matriculado
    matriculas = Matriculas.objects.filter(fk_estudiante=estudiante)

    # Total de clases
    total_clases = matriculas.count()

    # Módulos distintos asociados a las clases
    clases_ids = matriculas.values_list('fk_clase_id', flat=True)
    modulos_unicos = Modulos.objects.filter(clases__cla_id__in=clases_ids).distinct()
    total_modulos = modulos_unicos.count()

    # Avance por niveles
    avances = Avance_Matriculados.objects.filter(fk_matricula__fk_estudiante=estudiante)

    # Nota promedio
    promedio = avances.aggregate(promedio_nota=models.Avg('avm_nota_final'))['promedio_nota'] or 0

    # Niveles completados
    niveles_aprobados = avances.filter(avm_nota_final__gte=7).count()  # suponiendo que 7 es aprobado

    contexto = {
        'total_clases': total_clases,
        'total_modulos': total_modulos,
        'promedio': round(promedio, 2),
        'niveles_aprobados': niveles_aprobados,
        'nombre': request.user.first_name
    }

    return render(request, 'masterestudiante/core/Index.html', contexto)