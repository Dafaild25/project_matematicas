from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST
from ...models import IntentoNivel, Matriculas, Niveles,Avance_Matriculados, Vidas_Extras
from Aplicaciones.core.decorators import rol_required # Importar decorador para requerir docente

@require_GET

def historial_intentos(request):
    matricula_id = request.GET.get('matricula_id')
    nivel_id = request.GET.get('nivel_id')

    intentos = IntentoNivel.objects.filter(
        fk_matricula_id=matricula_id,
        fk_nivel_id=nivel_id
    ).order_by('-in_fecha_creacion')

    datos = []
    for intento in intentos:
        datos.append({
            'nota': str(intento.in_nota) if intento.in_nota is not None else '—',
            'vidas': intento.in_vidas_usadas or 0,
            'fecha': intento.in_fecha_creacion.strftime('%d-%m-%Y %H:%M'),
        })

    return JsonResponse({'success': True, 'intentos': datos})


@require_POST
@rol_required('docente')
def asignar_vidas(request):
    try:
        matricula_id = request.POST.get('matricula_id')
        nivel_id = request.POST.get('nivel_id')
        vidas = int(request.POST.get('vidas'))
        observaciones = request.POST.get('observaciones', '')

        matricula = Matriculas.objects.get(pk=matricula_id)
        nivel = Niveles.objects.get(pk=nivel_id)

        # Crear o actualizar la vida extra
        vidas_extra, creado = Vidas_Extras.objects.update_or_create(
            matricula=matricula,
            nivel=nivel,
            defaults={
                'vidas_asignadas': vidas,
                'asignado_por': request.user,
                'observaciones': observaciones,
                'vidas_aplicadas': False
            }
        )

        # Buscar el avance correspondiente
        avance = Avance_Matriculados.objects.filter(
            fk_matricula=matricula,
            fk_nivel=nivel
        ).first()

        if avance:
            vidas_aplicadas = avance.aplicar_vidas_extras_pendientes()
            return JsonResponse({'success': True, 'message': f'Vidas asignadas correctamente.'})
        else:
            return JsonResponse({'success': True, 'message': 'Vidas asignadas. Se aplicarán al iniciar el nivel.'})

    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})
