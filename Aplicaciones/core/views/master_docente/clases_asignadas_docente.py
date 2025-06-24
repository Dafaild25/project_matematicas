from django.shortcuts import render, get_object_or_404
from django.db.models import Count
from ...models import Clases, Estudiantes, Docentes, Matriculas, Personas
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

@login_required
def clases_asignadas_docente(request):
    # Obtener la persona vinculada al usuario logueado
    persona = get_object_or_404(Personas, fk_id_usuario=request.user)

    # Obtener el docente correspondiente
    docente = get_object_or_404(Docentes, fk_id_persona=persona)

    # Obtener las clases asignadas al docente
    clases = Clases.objects.filter(fk_docente=docente) \
        .annotate(num_matriculados=Count('matriculas'))

    return render(request, 'masterdocente/clase/Clase_Asignada.html', {
        'clases': clases
    })
    
    
    
@login_required    
def matriculados_asignados_docente(request,clase_id):
    # Obtener la persona vinculada al usuario logueado
    persona = get_object_or_404(Personas, fk_id_usuario=request.user)

    # Obtener el docente correspondiente
    docente = get_object_or_404(Docentes, fk_id_persona=persona)

    # Obtener las clases asignadas al docente
    clase = get_object_or_404(Clases, pk=clase_id, fk_docente=docente)
    # Obtener estudiantes matriculados en esa clase
    matriculas = Matriculas.objects.filter(fk_clase=clase).select_related('fk_estudiante')

    return render(request, 'masterdocente/clase/Matriculados_Asignados.html', {
        'clases': clase,
        'matriculas': matriculas
    })