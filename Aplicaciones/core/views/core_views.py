from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.db.models import Avg
from ..models import *

# Create your views here.
def dashboard_admin(request):
    # Totales
    total_docentes = Docentes.objects.count()
    total_modulos = Modulos.objects.count()
    modulos = Modulos.objects.all()

    contexto = {
        'total_docentes': total_docentes,
        'total_modulos': total_modulos,
        'modulos': modulos
    }
    return render(request, 'core/index.html', contexto)

def obtener_datos_admin(request):
    modulo_id = request.GET.get('modulo_id')
    if modulo_id:
        clases = Clases.objects.filter(fk_modulo_id=modulo_id)
    else:
        clases = Clases.objects.all()

    labels, docentes, values = [], [], []
    total, count = 0, 0

    for c in clases:
        # Promedio de la clase
        prom = Avance_Matriculados.objects.filter(
            fk_matricula__fk_clase=c
        ).aggregate(promedio=Avg('avm_nota_final'))['promedio']
        if prom is not None:
            labels.append(c.cla_nombre)
            docentes.append(c.fk_docente.fk_id_persona.fk_id_usuario.get_full_name())
            values.append(round(prom, 2))
            total += prom
            count += 1

    promedio_general = round(total / count, 2) if count else 0

    return JsonResponse({
        'labels': labels,
        'docentes': docentes,
        'values': values,
        'promedio_general': promedio_general
    })

