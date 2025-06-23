from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from ..models import IntentoNivel, Avance_Matriculados, Niveles, Matriculas
from django.db.models import Max
from django.utils import timezone



@login_required
@csrf_exempt
def get_game_info(request):
    """Obtener información del juego incluyendo vidas restantes"""
    try:
        data = json.loads(request.body)
        estudiante_id = data.get('estudiante_id')
        nivel_id = data.get('nivel_id')
        
        # Obtener el nivel
        nivel = get_object_or_404(Niveles, niv_id=nivel_id)
        
        # Obtener la matrícula del estudiante (necesaria para la relación)
        matricula = get_object_or_404(Matriculas, fk_estudiante_id=estudiante_id)
        
        # Obtener o crear el avance del estudiante
        avance, created = Avance_Matriculados.objects.get_or_create(
            fk_matricula=matricula,
            fk_nivel=nivel,
            defaults={
                'avm_estado': 'iniciado',
                'avm_vidas_restantes': nivel.niv_vidas,  # Asumiendo que el campo se llama niv_vidas
            }
        )
        
        # Si es la primera vez, inicializar vidas
        if created or avance.avm_vidas_restantes is None:
            avance.inicializar_vidas()
        
        # Verificar si hay vidas adicionales disponibles (si el admin aumentó las vidas)
        vidas_restauradas = avance.restaurar_vidas_por_cambio_admin()
        
        # Obtener número total de intentos realizados
        intentos_realizados = IntentoNivel.objects.filter(
            fk_matricula=matricula,
            fk_nivel=nivel
        ).count()
        
        mensaje_vidas = ""
        if vidas_restauradas > 0:
            mensaje_vidas = f"¡El profesor agregó {vidas_restauradas} vida(s) adicional(es)! "
        
        mensaje_vidas += f"Tienes {avance.avm_vidas_restantes} vidas restantes de {nivel.niv_vidas} totales"
        
        return JsonResponse({
            'success': True,
            'vidas_restantes': avance.avm_vidas_restantes,
            'vidas_totales': nivel.niv_vidas,
            'intentos_realizados': intentos_realizados,
            'puede_intentar': avance.puede_intentar(),
            'estado': avance.avm_estado,
            'vidas_restauradas': vidas_restauradas,
            'mensaje': mensaje_vidas
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })


@login_required
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
        matricula = get_object_or_404(Matriculas, fk_estudiante_id=estudiante_id)
        
        # Obtener el avance
        avance = get_object_or_404(Avance_Matriculados, 
                                 fk_matricula=matricula, 
                                 fk_nivel=nivel)
        
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

@login_required
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

@login_required
@csrf_exempt
def update_best_score(request):
    """Actualizar el mejor puntaje del estudiante"""
    try:
        data = json.loads(request.body)
        estudiante_id = data.get('estudiante_id')
        nivel_id = data.get('nivel_id')
        
        # Obtener matrícula
        matricula = get_object_or_404(Matriculas, fk_estudiante_id=estudiante_id)
        nivel = get_object_or_404(Niveles, niv_id=nivel_id)
        
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