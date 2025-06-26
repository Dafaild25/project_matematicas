from django.shortcuts import render
from django.db.models import Count, Avg
from django.http import JsonResponse
from ...models import *
from Aplicaciones.core.decorators import rol_required # Importar decorador para requerir docente

# Vista para obtener los datos dinámicos del dashboard (llamada por AJAX)
@rol_required('docente')
def obtener_datos_dashboard(request):
    docente = Docentes.objects.get(fk_id_persona__fk_id_usuario=request.user)
    modulo_id = request.GET.get('modulo_id')

    if modulo_id:
        clases = Clases.objects.filter(fk_docente=docente, fk_modulo_id=modulo_id)
    else:
        clases = Clases.objects.filter(fk_docente=docente)

    labels = []
    values = []
    total_notas = 0
    total_clases = 0

    for clase in clases:
        matriculas = Matriculas.objects.filter(fk_clase=clase)
        promedio_clase = Avance_Matriculados.objects.filter(
            fk_matricula__in=matriculas,
            fk_nivel__fk_modulo=clase.fk_modulo
        ).aggregate(promedio=Avg('avm_nota_final'))['promedio']

        if promedio_clase is not None:
            labels.append(clase.cla_nombre)
            values.append(round(promedio_clase, 2))
            total_notas += promedio_clase
            total_clases += 1

    if total_clases > 0:
        promedio_general = round(total_notas / total_clases, 2)
    else:
        promedio_general = 0

    return JsonResponse({
        'labels': labels,
        'values': values,
        'promedio_general': promedio_general
    })


# Dashboard Docente Principal
@rol_required('docente')
def dashboard_docente(request):
    docente = Docentes.objects.get(fk_id_persona__fk_id_usuario=request.user)

    total_clases = Clases.objects.filter(fk_docente=docente).count()

    total_estudiantes = Matriculas.objects.filter(
        fk_clase__fk_docente=docente
    ).values('fk_estudiante').distinct().count()

    modulos = Modulos.objects.all()

    promedio_estudiantes = Avance_Matriculados.objects.filter(
        fk_matricula__fk_clase__fk_docente=docente
    ).aggregate(promedio=Avg('avm_nota_final'))['promedio']

    context = {
        'total_clases': total_clases,
        'total_estudiantes': total_estudiantes,
        'promedio_estudiantes': float(promedio_estudiantes) if promedio_estudiantes else 0,
        'modulos': modulos
    }
    return render(request, 'masterdocente/core/Index.html', context)
