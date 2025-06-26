from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from easy_pdf.views import PDFTemplateResponse
from ...models import IntentoNivel, Matriculas, Niveles
import unicodedata
import re
from django.utils.decorators import method_decorator
from django.views import View


# Función auxiliar para limpiar nombre de archivo
def clean_filename(text):
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')
    return re.sub(r'[^\w\s-]', '', text).replace(' ', '_')


@method_decorator(login_required, name='dispatch')
class ReporteIntentoIndividualPDFView(View):

    def get(self, request, matricula_id, nivel_id):
        # Obtener los intentos del nivel
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
            matricula = get_object_or_404(Matriculas.objects.select_related('fk_estudiante'), pk=matricula_id)
            nivel = get_object_or_404(Niveles.objects.select_related('fk_modulo'), pk=nivel_id)
            estudiante = matricula.fk_estudiante
            modulo = nivel.fk_modulo

        estudiante_str = clean_filename(str(estudiante))
        nivel_str = clean_filename(nivel.niv_nombre)
        filename = f"intento_{estudiante_str}_nivel_{nivel_str}.pdf"

        context = {
            'intentos': intentos,
            'estudiante': estudiante,
            'nivel': nivel,
            'modulo': modulo
        }

        return PDFTemplateResponse(
            request=request,
            template='reporte-historial/reporte_intento_individual.html',
            filename=filename,
            context=context,
            show_content_in_browser=True
        )
