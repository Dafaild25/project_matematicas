
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from ..models import IntentoNivel, AvanceEstudiante,Niveles
from django.db.models import Max
from django.utils import timezone

def cuestionario_Modulo1(request):
    return render(request, 'cuestionario/cuestionario_Modulo1.html')
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
        
        # Obtener o crear el avance del estudiante
        avance, created = AvanceEstudiante.objects.get_or_create(
            estudiante_id=estudiante_id,
            nivel=nivel,
            defaults={
                'estado': 'iniciado',
                'vidas_restantes': nivel.vidas,
                'vidas_iniciales_nivel': nivel.vidas  # Establecer vidas iniciales
            }
        )
        
        # Si es la primera vez, inicializar vidas
        if created or avance.vidas_restantes is None:
            avance.inicializar_vidas()
        
        # Verificar si hay vidas adicionales disponibles (si el admin aumentó las vidas)
        vidas_restauradas = avance.restaurar_vidas_por_cambio_admin()
        
        # Obtener número total de intentos realizados
        intentos_realizados = IntentoNivel.objects.filter(
            estudiante_id=estudiante_id,
            nivel=nivel
        ).count()
        
        mensaje_vidas = ""
        if vidas_restauradas > 0:
            mensaje_vidas = f"¡El profesor agregó {vidas_restauradas} vida(s) adicional(es)! "
        
        mensaje_vidas += f"Tienes {avance.vidas_restantes} vidas restantes de {nivel.vidas} totales"
        
        return JsonResponse({
            'success': True,
            'vidas_restantes': avance.vidas_restantes,
            'vidas_totales': nivel.vidas,
            'intentos_realizados': intentos_realizados,
            'puede_intentar': avance.puede_intentar(),
            'estado': avance.estado,
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
        
        # Obtener el nivel y avance
        nivel = get_object_or_404(Niveles, niv_id=nivel_id)
        avance = get_object_or_404(AvanceEstudiante, 
                                 estudiante_id=estudiante_id, 
                                 nivel=nivel)
        
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
            estudiante_id=estudiante_id,
            nivel=nivel,
            nota=nota,
            vidas_usadas=1  # Siempre usa 1 vida por intento
        )
        
        # Actualizar estado del avance
        if nota >= 7:  # Aprobado
            avance.estado = 'aprobado'
            if avance.nota_final is None or nota > avance.nota_final:
                avance.nota_final = nota
        else:  # No aprobado
            if avance.vidas_restantes == 0:
                avance.estado = 'sin_vidas'
            else:
                avance.estado = 'en_progreso'
        
        avance.save()
        
        return JsonResponse({
            'success': True,
            'nota': nota,
            'vidas_restantes': avance.vidas_restantes,
            'estado': avance.estado,
            'puede_continuar': avance.puede_intentar(),
            'aprobado': nota >= 7,
            'mensaje': f"Intento guardado. Te quedan {avance.vidas_restantes} vidas."
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
        avance, created = AvanceEstudiante.objects.get_or_create(
            estudiante_id=estudiante_id,
            nivel=nivel,
            defaults={
                'estado': 'iniciado',
                'vidas_restantes': nivel.vidas
            }
        )
        
        if created:
            avance.inicializar_vidas()
        
        # Verificar si hay vidas adicionales
        vidas_restauradas = avance.restaurar_vidas_si_necesario()
        
        return JsonResponse({
            'success': True,
            'vidas_restantes': avance.vidas_restantes,
            'vidas_totales': nivel.vidas,
            'puede_intentar': avance.puede_intentar(),
            'estado': avance.estado,
            'vidas_restauradas': vidas_restauradas
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })

# MANTENER TU FUNCIÓN ORIGINAL update_best_score
@login_required
@csrf_exempt
def update_best_score(request):
    """Actualizar el mejor puntaje del estudiante"""
    try:
        data = json.loads(request.body)
        estudiante_id = data.get('estudiante_id')
        nivel_id = data.get('nivel_id')
        
        # Obtener el mejor intento
        mejor_intento = IntentoNivel.objects.filter(
            estudiante_id=estudiante_id,
            nivel_id=nivel_id
        ).order_by('-nota').first()
        
        if mejor_intento:
            # Actualizar el avance con la mejor nota
            avance = AvanceEstudiante.objects.get(
                estudiante_id=estudiante_id,
                nivel_id=nivel_id
            )
            avance.nota_final = mejor_intento.nota
            avance.save()
            
            return JsonResponse({
                'success': True,
                'best_score': float(mejor_intento.nota)
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
    
