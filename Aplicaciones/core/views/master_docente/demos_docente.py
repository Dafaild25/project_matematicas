# views.py - Vistas para docentes
from django.shortcuts import render, get_object_or_404
from django.template.loader import get_template, TemplateDoesNotExist
from ...decorators import docente_required
from ...models import Modulos, Niveles, User, Personas, Docentes


@docente_required
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



@docente_required 
def docente_probar_nivel(request, nivel_id):
    """Vista para que el docente pueda probar/ver un nivel sin guardar progreso"""
    
    print(f"🐛 === INICIO docente_probar_nivel ===")
    print(f"🐛 Usuario: {request.user}")
    print(f"🐛 nivel_id recibido: {nivel_id} (tipo: {type(nivel_id)})")
    
    nivel = get_object_or_404(Niveles, pk=nivel_id)
    print(f"🐛 Nivel encontrado: {nivel}")
    print(f"🐛 Módulo del nivel: {nivel.fk_modulo}")
    
    template_name = nivel.ruta
    print(f"🐛 Template a usar: {template_name}")
    
    try:
        get_template(template_name)
        print(f"✅ Template encontrado: {template_name}")
    except TemplateDoesNotExist:
        print(f"❌ Template NO encontrado: {template_name}")
        return render(request, "masterdocente/error.html", {
            "mensaje": "Nivel no disponible aún.",
            "es_docente": True
        })

    try:
        persona = Personas.objects.get(fk_id_usuario=request.user)
        docente = Docentes.objects.get(fk_id_persona=persona)
        print(f"✅ Docente encontrado: {docente}")
    except Personas.DoesNotExist:
        print(f"❌ Persona NO encontrada para usuario: {request.user}")
        return render(request, "masterdocente/error.html", {
            "mensaje": "No se encontró la persona del usuario.",
            "es_docente": True
        })
    except Docentes.DoesNotExist:
        print(f"❌ Docente NO encontrado para persona: {persona}")
        return render(request, "masterdocente/error.html", {
            "mensaje": "El usuario no está registrado como docente.",
            "es_docente": True
        })

    # ✅ CONVERTIR nivel_id a entero para evitar problemas
    try:
        nivel_id_int = int(nivel_id)
        print(f"✅ nivel_id convertido a int: {nivel_id_int}")
    except (ValueError, TypeError):
        nivel_id_int = nivel.niv_id
        print(f"⚠️ Error convirtiendo nivel_id, usando nivel.niv_id: {nivel_id_int}")

    # ✅ CONTEXTO COMPLETO PARA DOCENTE - CORREGIDO
    contexto = {
        'nivel': nivel,
        'modulo': nivel.fk_modulo,
        'modulo_id': nivel.fk_modulo.mod_id,
        'level_id': nivel_id_int,        # ✅ IMPORTANTE: Pasar level_id
        'matricula_id': -1,              # ✅ ID ficticio para docente
        'es_docente': True,              # ✅ CRÍTICO: Debe ser True
        'modo_prueba': True,             # ✅ CRÍTICO: Debe ser True
        'template_base': 'plantillas/MasterDocente.html',
        'docente': docente,
        'vidas_nivel': nivel.vidas,
        'mensaje_docente': f"Probando {nivel.niv_nombre} en modo docente"
    }

    print("🐛 === CONTEXTO FINAL ===")
    for key, value in contexto.items():
        print(f"🐛   {key}: {value} (tipo: {type(value)})")
    
    # ✅ VERIFICACIONES CRÍTICAS
    assert contexto['es_docente'] == True, "❌ es_docente debe ser True"
    assert contexto['modo_prueba'] == True, "❌ modo_prueba debe ser True"
    assert contexto['level_id'] > 0, "❌ level_id debe ser mayor a 0"
    assert contexto['modulo_id'] > 0, "❌ modulo_id debe ser mayor a 0"
    
    print("✅ Todas las verificaciones pasaron")
    print(f"🐛 === FIN docente_probar_nivel - Renderizando {template_name} ===")
    
    return render(request, template_name, contexto)