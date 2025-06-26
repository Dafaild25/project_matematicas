from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from ..models import IntentoNivel, Avance_Matriculados, Niveles, Matriculas,Vidas_Extras
from django.db.models import Max
from django.utils import timezone


# VISTA DE EJERCICIOS CORREGIDA

@csrf_exempt
def get_game_info(request):
    """Obtener información del juego incluyendo vidas restantes"""
    try:
        data = json.loads(request.body)
        estudiante_id = data.get('estudiante_id')
        nivel_id = data.get('nivel_id')
        
        # Obtener el nivel
        nivel = get_object_or_404(Niveles, niv_id=nivel_id)
        
        # SOLUCIÓN: Manejar múltiples matrículas
        try:
            # Primero intentar obtener una matrícula activa específica
            matricula = Matriculas.objects.get(fk_estudiante_id=estudiante_id)
        except Matriculas.MultipleObjectsReturned:
            # Si hay múltiples, usar criterios para elegir la correcta
            # Opción 1: La más reciente
            matricula = Matriculas.objects.filter(
                fk_estudiante_id=estudiante_id
            ).order_by('-mat_fecha_creacion').first()  # Ajusta el campo de fecha según tu modelo
            
            # Opción 2: Si tienes un campo de estado "activo"
            # matricula = Matriculas.objects.filter(
            #     fk_estudiante_id=estudiante_id,
            #     activo=True  # Si tienes este campo
            # ).first()
            
            # Opción 3: Si las matrículas están relacionadas con módulos específicos
            # nivel_modulo = nivel.fk_modulo  # Asumiendo que el nivel tiene módulo
            # matricula = Matriculas.objects.filter(
            #     fk_estudiante_id=estudiante_id,
            #     fk_modulo=nivel_modulo  # Si la matrícula está asociada a un módulo
            # ).first()
            
            if not matricula:
                return JsonResponse({
                    'success': False,
                    'error': 'No se encontró una matrícula válida para este estudiante'
                })
                
        except Matriculas.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': 'No se encontró matrícula para este estudiante'
            })
        
        # Obtener o crear el avance del estudiante
        avance, created = Avance_Matriculados.objects.get_or_create(
            fk_matricula=matricula,
            fk_nivel=nivel,
            defaults={
                'avm_estado': 'iniciado',
            }
        )
        
        # Solo inicializar vidas si es la primera vez o no tiene vidas asignadas
        if created or avance.avm_vidas_restantes is None:
            avance.inicializar_vidas()
        
        # VERIFICAR si hay vidas extras pendientes de aplicar (solo una vez)
        vidas_aplicadas = avance.aplicar_vidas_extras_pendientes()
        
        # Obtener información sobre vidas extras
        vidas_extras_info = None
        try:
            vidas_extras = Vidas_Extras.objects.get(
                matricula=matricula,
                nivel=nivel
            )
            vidas_extras_info = {
                'tiene_vidas_extras': True,
                'vidas_asignadas': vidas_extras.vidas_asignadas,
                'fecha_asignacion': vidas_extras.fecha_asignacion,
                'asignado_por': vidas_extras.asignado_por.username,
                'ya_aplicadas': vidas_extras.vidas_aplicadas
            }
        except Vidas_Extras.DoesNotExist:
            vidas_extras_info = {
                'tiene_vidas_extras': False,
                'vidas_asignadas': nivel.vidas,
                'ya_aplicadas': True
            }
        
        # Obtener número total de intentos realizados
        intentos_realizados = IntentoNivel.objects.filter(
            fk_matricula=matricula,
            fk_nivel=nivel
        ).count()
        
        # Construir mensaje sobre vidas
        mensaje_vidas = ""
        if vidas_aplicadas > 0:
            mensaje_vidas = f"¡El profesor te asignó {vidas_aplicadas} vida(s) adicional(es)! "
        
        if vidas_extras_info['tiene_vidas_extras']:
            mensaje_vidas += f"Tienes {avance.avm_vidas_restantes} vidas restantes de {vidas_extras_info['vidas_asignadas']} asignadas por el profesor"
        else:
            mensaje_vidas += f"Tienes {avance.avm_vidas_restantes} vidas restantes de {nivel.vidas} del nivel"
        
        return JsonResponse({
            'success': True,
            'vidas_restantes': avance.avm_vidas_restantes,
            'vidas_totales': vidas_extras_info['vidas_asignadas'],
            'vidas_originales_nivel': nivel.vidas,
            'intentos_realizados': intentos_realizados,
            'puede_intentar': avance.puede_intentar(),
            'estado': avance.avm_estado,
            'vidas_aplicadas_ahora': vidas_aplicadas,
            'tiene_vidas_extras': vidas_extras_info['tiene_vidas_extras'],
            'vidas_extras_info': vidas_extras_info,
            'mensaje': mensaje_vidas,
            'matricula_id': matricula.mat_id  # Agregar para debug
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })



# FUNCIÓN AUXILIAR PARA ASIGNAR VIDAS EXTRAS (para usar en admin o vista específica)


@csrf_exempt
def asignar_vidas_extras(request):
    """Vista para que el admin asigne vidas extras a un estudiante específico"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            matricula_id = data.get('matricula_id')
            nivel_id = data.get('nivel_id')
            vidas_asignadas = data.get('vidas_asignadas')
            observaciones = data.get('observaciones', '')
            
            # Validaciones básicas
            if not all([matricula_id, nivel_id, vidas_asignadas is not None]):
                return JsonResponse({
                    'success': False,
                    'error': 'Faltan datos requeridos'
                })
            
            if vidas_asignadas < 0:
                return JsonResponse({
                    'success': False,
                    'error': 'Las vidas no pueden ser negativas'
                })
            
            # Obtener objetos
            matricula = get_object_or_404(Matriculas, mat_id=matricula_id)
            nivel = get_object_or_404(Niveles, niv_id=nivel_id)
            
            # VALIDACIÓN CORREGIDA: No permitir asignar más vidas que las iniciales del nivel
            if vidas_asignadas > nivel.vidas:
                return JsonResponse({
                    'success': False,
                    'error': f'No se pueden asignar más de {nivel.vidas} vidas. El nivel "{nivel.niv_nombre}" tiene un máximo de {nivel.vidas} vidas.'
                })
            
            # Crear o actualizar vidas extras
            vidas_extras, created = Vidas_Extras.objects.update_or_create(
                matricula=matricula,
                nivel=nivel,
                defaults={
                    'vidas_asignadas': vidas_asignadas,
                    'asignado_por': request.user,
                    'observaciones': observaciones,
                    'vidas_aplicadas': False  # IMPORTANTE: Marcar como NO aplicadas
                }
            )
            
            # Obtener o crear el avance del estudiante
            avance, _ = Avance_Matriculados.objects.get_or_create(
                fk_matricula=matricula,
                fk_nivel=nivel,
                defaults={'avm_estado': 'iniciado'}
            )
            
            # Inicializar vidas si es necesario
            avance.inicializar_vidas()
            
            # Aplicar las vidas extras inmediatamente
            diferencia_vidas = avance.aplicar_vidas_extras_pendientes()
            
            accion = "creadas" if created else "actualizadas"
            
            return JsonResponse({
                'success': True,
                'message': f'Vidas extras {accion} correctamente. Estudiante: {matricula.fk_estudiante.username}, Nivel: {nivel.niv_nombre}, Vidas asignadas: {vidas_asignadas}',
                'diferencia_vidas': diferencia_vidas,
                'vidas_restantes': avance.avm_vidas_restantes,
                'vidas_maximas_nivel': nivel.vidas
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })
    
    return JsonResponse({
        'success': False,
        'error': 'Método no permitido'
    })



@csrf_exempt
def save_attempt(request):
    """Guardar intento y reducir una vida"""
    try:
        data = json.loads(request.body)
        estudiante_id = data.get('estudiante_id')
        nivel_id = data.get('nivel_id')
        puntaje_total = data.get('puntaje_total', 0)
        
        # Obtener el nivel y matrícula
        nivel = get_object_or_404(Niveles, niv_id=nivel_id)
        # Obtener avance (con acceso indirecto a la matrícula)
        avance = get_object_or_404(Avance_Matriculados,
                                   fk_matricula__fk_estudiante_id=estudiante_id,
                                   fk_nivel=nivel)
        matricula = avance.fk_matricula
        
        # Verificar si puede hacer el intento
        if not avance.puede_intentar():
            return JsonResponse({
                'success': False,
                'error': 'No tienes vidas restantes para este nivel'
            })
        
        # Usar una vida
        vida_usada = avance.usar_vida()
        
        if not vida_usada:
            return JsonResponse({
                'success': False,
                'error': 'No se pudo usar la vida'
            })
        
        # Calcular nota (puntaje_total ya viene de 0-10)
        nota = max(0, min(10, float(puntaje_total)))
        
        # Crear el intento
        intento = IntentoNivel.objects.create(
            fk_matricula=matricula,
            fk_nivel=nivel,
            in_nota=nota,
            in_vidas_usadas=1  # Siempre usa 1 vida por intento
        )
        
        # Actualizar estado del avance
        if nota >= 7:  # Aprobado
            avance.avm_estado = 'aprobado'
            if avance.avm_nota_final is None or nota > avance.avm_nota_final:
                avance.avm_nota_final = nota
        else:  # No aprobado
            if avance.avm_vidas_restantes == 0:
                avance.avm_estado = 'sin_vidas'
            else:
                avance.avm_estado = 'en_progreso'
        
        avance.save()
        
        return JsonResponse({
            'success': True,
            'nota': nota,
            'vidas_restantes': avance.avm_vidas_restantes,
            'estado': avance.avm_estado,
            'puede_continuar': avance.puede_intentar(),
            'aprobado': nota >= 7,
            'mensaje': f"Intento guardado. Te quedan {avance.avm_vidas_restantes} vidas."
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })


@csrf_exempt
def check_lives_status(request):
    """Verificar estado de vidas de un estudiante en un nivel"""
    try:
        data = json.loads(request.body)
        estudiante_id = data.get('estudiante_id')
        nivel_id = data.get('nivel_id')
        
        nivel = get_object_or_404(Niveles, niv_id=nivel_id)
        matricula = get_object_or_404(Matriculas, fk_estudiante_id=estudiante_id)
        
        avance, created = Avance_Matriculados.objects.get_or_create(
            fk_matricula=matricula,
            fk_nivel=nivel,
            defaults={
                'avm_estado': 'iniciado',
                'avm_vidas_restantes': nivel.niv_vidas
            }
        )
        
        if created:
            avance.inicializar_vidas()
        
        # Verificar si hay vidas adicionales
        vidas_restauradas = avance.restaurar_vidas_por_cambio_admin()
        
        return JsonResponse({
            'success': True,
            'vidas_restantes': avance.avm_vidas_restantes,
            'vidas_totales': nivel.niv_vidas,
            'puede_intentar': avance.puede_intentar(),
            'estado': avance.avm_estado,
            'vidas_restauradas': vidas_restauradas
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })


@csrf_exempt
def update_best_score(request):
    """Actualizar el mejor puntaje del estudiante"""
    try:
        data = json.loads(request.body)
        estudiante_id = data.get('estudiante_id')
        nivel_id = data.get('nivel_id')
        
     
        nivel = get_object_or_404(Niveles, niv_id=nivel_id)

         # Obtener avance único relacionado al estudiante y al nivel
        avance = get_object_or_404(
            Avance_Matriculados,
            fk_matricula__fk_estudiante_id=estudiante_id,
            fk_nivel=nivel
        )

        matricula = avance.fk_matricula
        
        # Obtener el mejor intento
        mejor_intento = IntentoNivel.objects.filter(
            fk_matricula=matricula,
            fk_nivel=nivel
        ).order_by('-in_nota').first()
        
        if mejor_intento:
            # Actualizar el avance con la mejor nota
            avance = Avance_Matriculados.objects.get(
                fk_matricula=matricula,
                fk_nivel=nivel
            )
            avance.avm_nota_final = mejor_intento.in_nota
            avance.save()
            
            return JsonResponse({
                'success': True,
                'best_score': float(mejor_intento.in_nota)
            })
        else:
            return JsonResponse({
                'success': False,
                'error': 'No se encontraron intentos'
            })
            
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })