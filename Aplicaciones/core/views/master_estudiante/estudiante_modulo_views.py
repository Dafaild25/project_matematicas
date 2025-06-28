from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.template.loader import get_template, TemplateDoesNotExist
from Aplicaciones.core.decorators import rol_required # Importar decorador para requerir estudiante
from ...models import Estudiantes, Matriculas,Modulos,Niveles,User,Personas


@rol_required('estudiante')
def estudiante_modulo(request):
    estudiante = Estudiantes.objects.get(fk_id_persona__fk_id_usuario=request.user)

    # Traer todas las clases del estudiante
    matriculas = Matriculas.objects.filter(fk_estudiante=estudiante).select_related('fk_clase__fk_modulo')

    # Extraer módulos únicos desde las clases
    modulos = set(matricula.fk_clase.fk_modulo for matricula in matriculas)

    contexto = {
        'modulos': modulos
    }
    return render(request, 'masterestudiante/modulo/Estudiante_Modulo.html', contexto)

@rol_required('estudiante')
def ver_niveles_modulo(request, modulo_id):
    estudiante = Estudiantes.objects.get(fk_id_persona__fk_id_usuario=request.user)
    
    modulo = get_object_or_404(Modulos, pk=modulo_id)

    # Filtrar solo niveles del módulo
    niveles = Niveles.objects.filter(fk_modulo=modulo).order_by('orden')

    contexto = {
        'modulo': modulo,
        'niveles': niveles,
        'modulo_id': modulo_id,  # ← AGREGAR ESTA LÍNEA
        'estudiante': estudiante
    }

    return render(request, 'masterestudiante/nivel/Estudiante_Nivel.html', contexto)



@rol_required('estudiante')
def jugar_nivel(request, nivel_id):
    nivel = get_object_or_404(Niveles, pk=nivel_id)
    template_name = nivel.ruta  # ej. "estudiante/nivel_1.html"

    try:
        get_template(template_name)
    except TemplateDoesNotExist:
        return render(request, "masterestudiante/error.html", {"mensaje": "Nivel no disponible aún."})

    matricula_id = None

    try:
        persona = Personas.objects.get(fk_id_usuario=request.user)
        estudiante = Estudiantes.objects.get(fk_id_persona=persona)
        matricula = Matriculas.objects.filter(fk_estudiante=estudiante, mat_estado=True).first()
        if matricula:
            matricula_id = matricula.mat_id
    except Personas.DoesNotExist:
        return render(request, "masterestudiante/error.html", {"mensaje": "No se encontró la persona del usuario."})
    except Estudiantes.DoesNotExist:
        return render(request, "masterestudiante/error.html", {"mensaje": "El usuario no está registrado como estudiante."})

    return render(request, template_name, {
        'nivel': nivel,
        'modulo': nivel.fk_modulo,
        'modulo_id': nivel.fk_modulo.mod_id,
        'student_id': request.user.id,
        'level_id': nivel_id,
        'matricula_id': matricula_id,
        'es_docente': False,
        'modo_prueba': False,
        'template_base': 'plantillas/MasterEstudiante.html',  # ✅ CLAVE: pasar plantilla base
    })
    