from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
from django.db.models import Avg
from django.views.decorators.http import require_http_methods
import logging
from ..models import *
from ..decorators import admin_required, docente_required, estudiante_required, ajax_required

# Configurar logger
logger = logging.getLogger('Aplicaciones.core.views')

# ===== VISTAS PROTEGIDAS =====

@admin_required
@require_http_methods(["GET"])
def dashboard_admin(request):
    """Dashboard para administradores"""
    try:
        logger.info(f"Usuario {request.user.username} accedió al dashboard admin")
        
        # Tu lógica original
        total_docentes = Docentes.objects.count()
        total_modulos = Modulos.objects.count()
        modulos = Modulos.objects.all()

        contexto = {
            'total_docentes': total_docentes,
            'total_modulos': total_modulos,
            'modulos': modulos,
            'user': request.user,
            'titulo': 'Dashboard Administrativo'
        }
        
        # Mensaje de bienvenida seguro
        try:
            if not request.session.get('welcome_shown'):
                messages.success(request, f'Bienvenido al dashboard, {request.user.get_full_name() or request.user.username}')
                request.session['welcome_shown'] = True
        except Exception as e:
            logger.warning(f"No se pudo mostrar mensaje de bienvenida: {e}")
        
        return render(request, 'core/index.html', contexto)
        
    except Exception as e:
        logger.error(f"Error en dashboard_admin: {e}")
        try:
            messages.error(request, 'Ocurrió un error al cargar el dashboard')
        except:
            pass
        return redirect('loguin_index')

@admin_required
@ajax_required
@require_http_methods(["GET"])
def obtener_datos_admin(request):
    """Obtener datos para gráficos del dashboard admin"""
    try:
        logger.debug(f"Usuario {request.user.username} solicitando datos admin")
        
        modulo_id = request.GET.get('modulo_id')
        
        # Validar modulo_id si se proporciona
        if modulo_id:
            try:
                modulo_id = int(modulo_id)
                clases = Clases.objects.filter(fk_modulo_id=modulo_id)
            except (ValueError, TypeError):
                logger.warning(f"modulo_id inválido: {modulo_id}")
                return JsonResponse({'error': 'ID de módulo inválido'}, status=400)
        else:
            clases = Clases.objects.all()

        labels, docentes, values = [], [], []
        total, count = 0, 0

        for c in clases:
            try:
                # Promedio de la clase
                prom = Avance_Matriculados.objects.filter(
                    fk_matricula__fk_clase=c
                ).aggregate(promedio=Avg('avm_nota_final'))['promedio']
                
                if prom is not None:
                    labels.append(c.cla_nombre)
                    # Verificar que el docente y sus relaciones existan
                    if hasattr(c, 'fk_docente') and c.fk_docente:
                        if hasattr(c.fk_docente, 'fk_id_persona') and c.fk_docente.fk_id_persona:
                            if hasattr(c.fk_docente.fk_id_persona, 'fk_id_usuario') and c.fk_docente.fk_id_persona.fk_id_usuario:
                                docente_nombre = c.fk_docente.fk_id_persona.fk_id_usuario.get_full_name()
                                if not docente_nombre:
                                    docente_nombre = c.fk_docente.fk_id_persona.fk_id_usuario.username
                            else:
                                docente_nombre = "Sin usuario asignado"
                        else:
                            docente_nombre = "Sin persona asignada"
                    else:
                        docente_nombre = "Sin docente asignado"
                    
                    docentes.append(docente_nombre)
                    values.append(round(prom, 2))
                    total += prom
                    count += 1
                    
            except Exception as e:
                logger.warning(f"Error procesando clase {c.id}: {e}")
                continue

        promedio_general = round(total / count, 2) if count else 0

        response_data = {
            'labels': labels,
            'docentes': docentes,
            'values': values,
            'promedio_general': promedio_general,
            'total_clases': count
        }
        
        logger.debug(f"Datos enviados: {len(labels)} clases procesadas")
        return JsonResponse(response_data)
        
    except Exception as e:
        logger.error(f"Error en obtener_datos_admin: {e}")
        return JsonResponse({'error': 'Error interno del servidor'}, status=500)

# ===== VISTAS ADICIONALES PARA OTROS ROLES =====

@docente_required
def dashboard_docente(request):
    """Dashboard para docentes"""
    try:
        logger.info(f"Usuario {request.user.username} accedió al dashboard docente")
        
        contexto = {
            'user': request.user,
            'titulo': 'Dashboard Docente',
        }
        
        return render(request, 'docente/dashboard.html', contexto)
        
    except Exception as e:
        logger.error(f"Error en dashboard_docente: {e}")
        return redirect('loguin_index')

@estudiante_required
def core_estudiante(request):
    """Dashboard para estudiantes"""
    try:
        logger.info(f"Usuario {request.user.username} accedió al dashboard estudiante")
        
        contexto = {
            'user': request.user,
            'titulo': 'Dashboard Estudiante',
        }
        
        return render(request, 'estudiante/dashboard.html', contexto)
        
    except Exception as e:
        logger.error(f"Error en core_estudiante: {e}")
        return redirect('loguin_index')

# ===== VISTA DE MANEJO DE ERRORES =====
def handle_permission_denied(request):
    """Manejar accesos denegados"""
    try:
        messages.error(request, 'No tienes permisos para acceder a esa página')
    except:
        pass
    return redirect('loguin_index')