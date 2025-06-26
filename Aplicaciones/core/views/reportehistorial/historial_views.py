from django.template.loader import get_template
from xhtml2pdf import pisa
from django.http import HttpResponse
from ...models import IntentoNivel, Matriculas, Niveles
import unicodedata
import re
from django.contrib.auth.decorators import login_required

# Utilidad para limpiar nombres (sin acentos ni espacios raros)
def clean_filename(text):
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')
    return re.sub(r'[^\w\s-]', '', text).replace(' ', '_')

@login_required
def generar_reporte_intento_individual_pdf(request, matricula_id, nivel_id):
    # Obtener intentos
    intentos = IntentoNivel.objects.select_related(
        'fk_matricula__fk_estudiante',
        'fk_nivel__fk_modulo'
    ).filter(
        fk_matricula_id=matricula_id,
        fk_nivel_id=nivel_id
    ).order_by('-in_fecha_creacion')

    intento_sample = intentos.first()

    if intento_sample:
        estudiante = intento_sample.fk_matricula.fk_estudiante
        nivel = intento_sample.fk_nivel
        modulo = nivel.fk_modulo
    else:
        # No hay intentos, se cargan datos base directamente
        matricula = Matriculas.objects.select_related('fk_estudiante').get(pk=matricula_id)
        nivel = Niveles.objects.select_related('fk_modulo').get(pk=nivel_id)
        estudiante = matricula.fk_estudiante
        modulo = nivel.fk_modulo

    # Renderizar plantilla con o sin datos
    template = get_template('reporte-historial/reporte_intento_individual.html')
    html = template.render({
        'intentos': intentos,
        'estudiante': estudiante,
        'nivel': nivel,
        'modulo': modulo
    })

    # Nombre del archivo
    estudiante_str = clean_filename(str(estudiante))
    nivel_str = clean_filename(nivel.niv_nombre)
    filename = f"intento_{estudiante_str}_nivel_{nivel_str}.pdf"

    # Generar PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse("Error al generar el PDF", status=500)
    return response