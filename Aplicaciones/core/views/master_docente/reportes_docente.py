from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.template.loader import get_template
from django.template import Context
from weasyprint import HTML
from django.conf import settings
from datetime import datetime
import os

# Importar tus modelos
from ...models import Clases, Niveles, Matriculas, Avance_Matriculados, IntentoNivel

@login_required
def generar_pdf_nivel(request, clase_id, nivel_id):
    """Genera PDF para un nivel específico usando template HTML"""
    clase = get_object_or_404(Clases, cla_id=clase_id)
    nivel = get_object_or_404(Niveles, niv_id=nivel_id)
    
    # Obtener datos de avance para este nivel
    matriculas = Matriculas.objects.filter(fk_clase=clase, mat_estado=True)
    
    avance_data = []
    notas_para_promedio = []
    
    for matricula in matriculas:
        estudiante = matricula.fk_estudiante
        try:
            avance = Avance_Matriculados.objects.get(
                fk_matricula=matricula,
                fk_nivel=nivel
            )
            intentos = IntentoNivel.objects.filter(
                fk_matricula=matricula,
                fk_nivel=nivel
            ).count()
            
            nota = avance.avm_nota_final or 0
            if nota > 0:
                notas_para_promedio.append(nota)
            
            avance_data.append({
                'estudiante': estudiante,
                'nota': nota,
                'estado': avance.get_avm_estado_display(),
                'vidas_restantes': avance.avm_vidas_restantes or 0,
                'intentos': intentos,
                'ultimo_intento': avance.avm_ultimo_intento
            })
        except Avance_Matriculados.DoesNotExist:
            avance_data.append({
                'estudiante': estudiante,
                'nota': 0,
                'estado': 'Sin iniciar',
                'vidas_restantes': nivel.vidas,
                'intentos': 0,
                'ultimo_intento': None
            })
    
    # Calcular promedio general del nivel
    promedio_general = round(sum(notas_para_promedio) / len(notas_para_promedio), 1) if notas_para_promedio else 0
    
    # Contar estados para estadísticas
    estados_count = {}
    for item in avance_data:
        estado = item['estado']
        estados_count[estado] = estados_count.get(estado, 0) + 1
    
    # Preparar contexto para el template
    context = {
        'clase': clase,
        'nivel': nivel,
        'avance_data': avance_data,
        'promedio_general': promedio_general,
        'total_estudiantes': len(avance_data),
        'estudiantes_con_nota': len(notas_para_promedio),
        'estados_count': estados_count,
        'fecha_reporte': datetime.now(),
        'docente_nombre': f"{clase.fk_docente.fk_id_persona.fk_id_usuario.first_name} {clase.fk_docente.fk_id_persona.fk_id_usuario.last_name}"
    }
    
    # Renderizar template
    template = get_template('reportes/pdf_nivel.html')
    html_string = template.render(context)
    
    # Generar PDF
    html = HTML(string=html_string, base_url=request.build_absolute_uri())
    pdf = html.write_pdf()
    
    # Preparar respuesta para visualizar en línea (no descargar)
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="avance_{clase.cla_nombre}_{nivel.niv_nombre}.pdf"'
    
    return response

@login_required
def generar_pdf_general(request, clase_id):
    """Genera PDF general con todos los niveles usando template HTML"""
    clase = get_object_or_404(Clases, cla_id=clase_id)
    niveles = Niveles.objects.filter(fk_modulo=clase.fk_modulo, niv_estado=True).order_by('orden')
    
    # Obtener datos completos
    matriculas = Matriculas.objects.filter(fk_clase=clase, mat_estado=True)
    
    avance_data = []
    promedios_por_nivel = {}
    
    for matricula in matriculas:
        estudiante = matricula.fk_estudiante
        niveles_data = []
        
        for nivel in niveles:
            try:
                avance = Avance_Matriculados.objects.get(
                    fk_matricula=matricula,
                    fk_nivel=nivel
                )
                nota = avance.avm_nota_final or 0
                niveles_data.append({
                    'nivel_id': nivel.niv_id,
                    'nota': nota,
                    'estado': avance.get_avm_estado_display(),
                    'vidas_restantes': avance.avm_vidas_restantes or 0
                })
                    
            except Avance_Matriculados.DoesNotExist:
                niveles_data.append({
                    'nivel_id': nivel.niv_id,
                    'nota': 0,
                    'estado': 'Sin iniciar',
                    'vidas_restantes': nivel.vidas
                })
        
        avance_data.append({
            'estudiante': estudiante,
            'matricula_id': matricula.mat_id,
            'niveles': niveles_data
        })
    
    # Calcular promedios por nivel
    for nivel in niveles:
        notas_nivel = []
        for fila in avance_data:
            for nivel_data in fila['niveles']:
                if nivel_data['nivel_id'] == nivel.niv_id and nivel_data['nota'] > 0:
                    notas_nivel.append(nivel_data['nota'])
        
        promedio = sum(notas_nivel) / len(notas_nivel) if notas_nivel else 0
        promedios_por_nivel[nivel.niv_id] = round(promedio, 1)
    
    # Calcular promedio general: suma de promedios por nivel / número de niveles
    promedios_validos = [promedio for promedio in promedios_por_nivel.values() if promedio > 0]
    promedio_general_total = round(sum(promedios_validos) / len(promedios_validos), 1) if promedios_validos else 0
    
    # Crear lista de niveles con sus promedios para el template
    niveles_con_promedios = []
    for nivel in niveles:
        niveles_con_promedios.append({
            'nivel': nivel,
            'promedio': promedios_por_nivel[nivel.niv_id]
        })
    
    # Preparar contexto para el template
    context = {
        'clase': clase,
        'niveles': niveles,
        'niveles_con_promedios': niveles_con_promedios,  # Nueva variable
        'avance_data': avance_data,
        'promedios_por_nivel': promedios_por_nivel,
        'promedio_general_total': promedio_general_total,
        'total_estudiantes': len(avance_data),
        'total_niveles': len(niveles),
        'fecha_reporte': datetime.now(),
        'docente_nombre': f"{clase.fk_docente.fk_id_persona.fk_id_usuario.first_name} {clase.fk_docente.fk_id_persona.fk_id_usuario.last_name}"
    }
    
    # Renderizar template
    template = get_template('reportes/pdf_general.html')
    html_string = template.render(context)
    
    # Generar PDF
    html = HTML(string=html_string, base_url=request.build_absolute_uri())
    pdf = html.write_pdf()
    
    # Preparar respuesta para visualizar en línea (no descargar)
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="avance_general_{clase.cla_nombre}.pdf"'
    
    return response