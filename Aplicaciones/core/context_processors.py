# tu_app/context_processors.py

from .models import Administradores, Docentes, Estudiantes, Personas

def foto_perfil_usuario(request):
    if request.user.is_authenticated:
        try:
            persona = Personas.objects.get(fk_id_usuario=request.user)
        except Personas.DoesNotExist:
            return {'foto_perfil': None}

        # Buscar foto como administrador
        administrador = Administradores.objects.filter(fk_id_persona=persona).first()
        if administrador and administrador.adm_fotografia:
            return {'foto_perfil': administrador.adm_fotografia.url}

        # Buscar foto como docente
        docente = Docentes.objects.filter(fk_id_persona=persona).first()
        if docente and docente.doc_fotografia:
            return {'foto_perfil': docente.doc_fotografia.url}

        # Buscar foto como estudiante
        estudiante = Estudiantes.objects.filter(fk_id_persona=persona).first()
        if estudiante and estudiante.est_fotografia:
            return {'foto_perfil': estudiante.est_fotografia.url}

    return {'foto_perfil': None}
