from django.shortcuts import render
from django.shortcuts import get_object_or_404
from ..models import Matriculas, Matriculas, Clases,Niveles,Avance_Matriculados
from django.db.models import Avg
from ..decorators import admin_required

@admin_required
def index(request, cla_id):
    clase = get_object_or_404(Clases, pk=cla_id)
    niveles = Niveles.objects.filter(fk_modulo=clase.fk_modulo).order_by('orden')
    matriculas = Matriculas.objects.filter(fk_clase=cla_id).order_by(
        'fk_estudiante__fk_id_persona__fk_id_usuario__last_name',
        'fk_estudiante__fk_id_persona__per_segundo_apellido'
    )

    data = []
    for matricula in matriculas:
        fila = {
            'estudiante': matricula.fk_estudiante,
            'matricula_id': matricula.mat_id, 
            'niveles': []
        }
        for nivel in niveles:
            avance = Avance_Matriculados.objects.filter(
                fk_matricula=matricula,
                fk_nivel=nivel
            ).first()

            if avance:
                fila['niveles'].append({
                    'nivel_id': nivel.niv_id,  
                    'nivel': nivel.niv_nombre,
                    'nota': avance.avm_nota_final,
                    'estado': '✅' if avance.avm_estado else '❌'
                })
            else:
                fila['niveles'].append({
                    'nivel_id': nivel.niv_id,  
                    'nivel': nivel.niv_nombre,
                    'nota': 'Sin jugar',
                    'estado': '—',
                    'nivel_estado':nivel.niv_estado
                })
        data.append(fila)
        
    # Calcular promedios por nivel
    promedios_por_nivel = {}
    for nivel in niveles:
        promedio = Avance_Matriculados.objects.filter(
            fk_matricula__fk_clase=clase,
            fk_nivel=nivel,
            avm_nota_final__isnull=False
        ).aggregate(prom=Avg('avm_nota_final'))['prom']

        promedios_por_nivel[nivel.niv_id] = round(promedio, 2) if promedio is not None else "-"

    return render(request, 'avance/Index.html', {
        'clase': clase,
        'niveles': niveles,
        'avance_data': data,
        'promedios_por_nivel': promedios_por_nivel
    })