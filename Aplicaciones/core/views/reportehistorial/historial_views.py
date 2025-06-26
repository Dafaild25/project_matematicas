from django.template.loader import get_template
from xhtml2pdf import pisa
from django.http import HttpResponse
from ...models import IntentoNivel
import unicodedata
import re

# Utilidad para limpiar nombres (sin acentos ni espacios raros)
def clean_filename(text):
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')
    return re.sub(r'[^\w\s-]', '', text).replace(' ', '_')

def generar_reporte_intento_individual_pdf(request, matricula_id, nivel_id):
    intentos = IntentoNivel.objects.select_related(
        'fk_matricula__fk_estudiante',
        'fk_nivel__fk_modulo'
    ).filter(
        fk_matricula_id=matricula_id,
        fk_nivel_id=nivel_id
    ).order_by('-in_fecha_creacion')

    if not intentos.exists():
        return HttpResponse("No hay intentos para esta combinación.", status=404)

    intento_sample = intentos.first()
    estudiante = intento_sample.fk_matricula.fk_estudiante
    nivel = intento_sample.fk_nivel
    modulo = nivel.fk_modulo

    template = get_template('reporte-historial/reporte_intento_individual.html')
    html = template.render({
        'intentos': intentos,
        'estudiante': estudiante,
        'nivel': nivel,
        'modulo': modulo
    })

    # Limpiar y construir nombre de archivo
    estudiante_str = clean_filename(str(estudiante))
    nivel_str = clean_filename(nivel.niv_nombre)
    filename = f"intento_{estudiante_str}_nivel_{nivel_str}.pdf"

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse("Error al generar el PDF", status=500)
    return response
