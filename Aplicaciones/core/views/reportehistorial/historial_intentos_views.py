from django.http import HttpResponse
from django.template.loader import get_template
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from datetime import datetime
import unicodedata
import re
from weasyprint import HTML
from ...models import IntentoNivel, Matriculas, Niveles
from ...decorators import docente_required,admin_required

# Limpiar nombre de archivo
def clean_filename(text):
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')
    return re.sub(r'[^\w\s-]', '', text).replace(' ', '_')


@docente_required
def generar_reporte_intento_individual_pdf(request, matricula_id, nivel_id):
    intentos = IntentoNivel.objects.select_related(
        'fk_matricula__fk_estudiante',
        'fk_nivel__fk_modulo'
    ).filter(
        fk_matricula_id=matricula_id,
        fk_nivel_id=nivel_id
    ).order_by('-in_fecha_creacion')

    if intentos.exists():
        intento_sample = intentos.first()
        estudiante = intento_sample.fk_matricula.fk_estudiante
        nivel = intento_sample.fk_nivel
        modulo = nivel.fk_modulo
    else:
        matricula = get_object_or_404(Matriculas.objects.select_related('fk_estudiante'), pk=matricula_id)
        nivel = get_object_or_404(Niveles.objects.select_related('fk_modulo'), pk=nivel_id)
        estudiante = matricula.fk_estudiante
        modulo = nivel.fk_modulo

    context = {
        'intentos': intentos,
        'estudiante': estudiante,
        'nivel': nivel,
        'modulo': modulo,
        'fecha_reporte': datetime.now(),
    }

    template = get_template('reporte-historial/reporte_intento_individual.html')
    html_string = template.render(context)
    pdf = HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf()

    filename = f"intento_{clean_filename(str(estudiante))}_nivel_{clean_filename(nivel.niv_nombre)}.pdf"
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="{filename}"'
    return response




@admin_required
def generar_reporte_intento_individual_admin_pdf(request, matricula_id, nivel_id):
    intentos = IntentoNivel.objects.select_related(
        'fk_matricula__fk_estudiante',
        'fk_nivel__fk_modulo'
    ).filter(
        fk_matricula_id=matricula_id,
        fk_nivel_id=nivel_id
    ).order_by('-in_fecha_creacion')

    if intentos.exists():
        intento_sample = intentos.first()
        estudiante = intento_sample.fk_matricula.fk_estudiante
        nivel = intento_sample.fk_nivel
        modulo = nivel.fk_modulo
    else:
        matricula = get_object_or_404(Matriculas.objects.select_related('fk_estudiante'), pk=matricula_id)
        nivel = get_object_or_404(Niveles.objects.select_related('fk_modulo'), pk=nivel_id)
        estudiante = matricula.fk_estudiante
        modulo = nivel.fk_modulo

    context = {
        'intentos': intentos,
        'estudiante': estudiante,
        'nivel': nivel,
        'modulo': modulo,
        'fecha_reporte': datetime.now(),
    }

    template = get_template('reporte-historial/reporte_intento_individual.html')
    html_string = template.render(context)
    pdf = HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf()

    filename = f"intento_{clean_filename(str(estudiante))}_nivel_{clean_filename(nivel.niv_nombre)}.pdf"
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="{filename}"'
    return response