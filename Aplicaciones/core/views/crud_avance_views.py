from django.shortcuts import render
from django.shortcuts import get_object_or_404
from ..models import Matriculas, Matriculas, Clases,Niveles,Avance_Matriculados

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
            'niveles': []
        }
        for nivel in niveles:
            avance = Avance_Matriculados.objects.filter(
                fk_matricula=matricula,
                fk_nivel=nivel
            ).first()

            if avance:
                fila['niveles'].append({
                    'nivel': nivel.niv_nombre,
                    'nota': avance.avm_nota_final,
                    'estado': '✅' if avance.avm_estado else '❌'
                })
            else:
                fila['niveles'].append({
                    'nivel': nivel.niv_nombre,
                    'nota': 'Sin jugar',
                    'estado': '—',
                    'nivel_estado':nivel.niv_estado
                })
        data.append(fila)

    return render(request, 'avance/Index.html', {
        'clase': clase,
        'niveles': niveles,
        'avance_data': data
    })