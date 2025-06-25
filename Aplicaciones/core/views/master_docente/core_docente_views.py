from django.shortcuts import render
from django.db.models import Count, Avg 
from django.contrib.auth.models import User # Importar modelo User de Django
from ...models import *
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
@csrf_exempt
def datos_modulo(request):
    if request.method == 'POST':
        modulo_id = request.POST.get('modulo_id')

        clases = Clases.objects.filter(fk_modulo_id=modulo_id)
        data_barras = []
        for clase in clases:
            total_estudiantes = Matriculas.objects.filter(fk_clase=clase).count()
            data_barras.append({'clase': clase.cla_nombre, 'total': total_estudiantes})

        promedio = Avance_Matriculados.objects.filter(
            fk_matricula__fk_clase__fk_modulo_id=modulo_id
        ).aggregate(promedio=Avg('avm_nota_final'))['promedio']

        return JsonResponse({
            'barras': data_barras,
            'promedio': float(promedio) if promedio else 0
        })
    return JsonResponse({'error': 'Método no permitido'}, status=405)



# DASHBOARD DOCENTE
def dashboard_docente(request):
    # Obtener docente actual
    docente = Docentes.objects.get(fk_id_persona__fk_id_usuario=request.user)

    # Número de clases
    total_clases = Clases.objects.filter(fk_docente=docente).count()

    # Número de estudiantes (sin duplicados)
    total_estudiantes = Matriculas.objects.filter(fk_clase__fk_docente=docente).values('fk_estudiante').distinct().count()

    # Estudiantes por módulo
    estudiantes_por_modulo = Matriculas.objects.filter(
        fk_clase__fk_docente=docente
    ).values(
        'fk_clase__fk_modulo__mod_nombre'
    ).annotate(total=Count('fk_estudiante'))

    # Promedio general
    promedio_estudiantes = Avance_Matriculados.objects.filter(
        fk_matricula__fk_clase__fk_docente=docente
    ).aggregate(promedio=Avg('avm_nota_final'))['promedio']

    modulos = Modulos.objects.all()

   
    # Enviar datos al template
    context = {
        'total_clases': total_clases,
        'total_estudiantes': total_estudiantes,
        'estudiantes_por_modulo': list(estudiantes_por_modulo),
        'promedio_estudiantes': float(promedio_estudiantes) if promedio_estudiantes else 0,
        'modulos': modulos
    }
    return render(request, 'masterdocente/core/Index.html',context );  

def core_docente(request):
    return render(request, 'masterdocente/core/Index.html' );  