# views.py - Vistas para docentes
from django.shortcuts import render, get_object_or_404
from django.template.loader import get_template, TemplateDoesNotExist
from Aplicaciones.core.decorators import rol_required
from ...models import Modulos, Niveles, User, Personas, Docentes


@rol_required('docente')
def docente_ver_niveles_modulo(request, modulo_id):
    """Vista para que el docente vea todos los niveles de un módulo específico"""
    
    docente = Docentes.objects.get(fk_id_persona__fk_id_usuario=request.user)
    modulo = get_object_or_404(Modulos, pk=modulo_id)

    # Obtener todos los niveles del módulo
    niveles = Niveles.objects.filter(fk_modulo=modulo).order_by('orden')

    contexto = {
        'modulo': modulo,
        'niveles': niveles,
        'modulo_id': modulo_id,
        'docente': docente,
        'es_docente': True  # Flag para identificar que es vista de docente
    }

    return render(request, 'masterdocente/demos/nivel/Docente_Nivel.html', contexto)




@rol_required('docente')
def docente_probar_nivel(request, nivel_id):
    """Vista para que el docente pueda probar/ver un nivel sin guardar progreso"""
    
    nivel = get_object_or_404(Niveles, pk=nivel_id)
    
    # ✅ AQUÍ ESTÁ LA CLAVE: Verificar si existe un template específico para docente
    # Primero intentar template específico de docente
    template_docente = f"masterdocente/niveles/{nivel.ruta}"
    template_estudiante = nivel.ruta  # ej. "estudiante/nivel_1.html"
    
    # Intentar cargar template de docente primero
    try:
        get_template(template_docente)
        template_name = template_docente
        print(f"✅ Usando template de docente: {template_docente}")
    except TemplateDoesNotExist:
        # Si no existe template de docente, usar el de estudiante con contexto de docente
        try:
            get_template(template_estudiante)
            template_name = template_estudiante
            print(f"⚠️ Usando template de estudiante en modo docente: {template_estudiante}")
        except TemplateDoesNotExist:
            return render(request, "masterdocente/error.html", {
                "mensaje": "Nivel no disponible aún.",
                "es_docente": True
            })

    try:
        persona = Personas.objects.get(fk_id_usuario=request.user)
        docente = Docentes.objects.get(fk_id_persona=persona)
    except Personas.DoesNotExist:
        return render(request, "masterdocente/error.html", {
            "mensaje": "No se encontró la persona del usuario.",
            "es_docente": True
        })
    except Docentes.DoesNotExist:
        return render(request, "masterdocente/error.html", {
            "mensaje": "El usuario no está registrado como docente.",
            "es_docente": True
        })

    # ✅ CONTEXTO ESPECIAL PARA DOCENTE
    contexto = {
        'nivel': nivel,
        'modulo': nivel.fk_modulo,
        'modulo_id': nivel.fk_modulo.mod_id,
        'docente_id': request.user.id,
        'level_id': nivel_id,
        'es_docente': True,           # 🔥 FLAG PRINCIPAL
        'modo_prueba': True,          # 🔥 FLAG SECUNDARIO
        'usar_plantilla_docente': True,  # 🔥 FLAG PARA PLANTILLA
        'docente': docente,
        'vidas_nivel': nivel.vidas,
        'mensaje_docente': f"Probando {nivel.niv_nombre} en modo docente"
        # NO se pasa matricula_id porque el docente no tiene matrícula
    }

    return render(request, template_name, contexto)