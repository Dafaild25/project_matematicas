from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from ..models import Matriculas, Estudiantes, Clases
from ..forms.matricula_form import MatriculasForm

def index(request):
    matriculas = Matriculas.objects.all()
    form = MatriculasForm()

    if request.method == 'POST':
        if 'crear_matricula' in request.POST:
            form = MatriculasForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Matrícula creada correctamente.')
                return redirect('matricula_index')
        elif 'editar_matricula' in request.POST:
            mat_id = request.POST.get('mat_id')
            matricula = get_object_or_404(Matriculas, pk=mat_id)

            # Editar manualmente los campos
            matricula.fk_clase_id = request.POST.get('fk_clase')
            matricula.fk_estudiante_id = request.POST.get('fk_estudiante')
            matricula.mat_estado = 'mat_estado' in request.POST
            matricula.save()

            messages.success(request, 'Matrícula actualizada correctamente.')
            return redirect('matricula_index')

        elif 'eliminar_matricula' in request.POST:
            mat_id = request.POST.get('mat_id')
            matricula = get_object_or_404(Matriculas, pk=mat_id)
            matricula.delete()
            messages.success(request, 'Matrícula eliminada correctamente.')
        return redirect('matricula_index')

    estudiantes = Estudiantes.objects.all()
    clases = Clases.objects.filter(cla_estado=True)

    return render(request, 'matricula/Index.html', {
        'matriculas': matriculas,
        'form': form,
        'estudiantes': estudiantes,
        'clases': clases,
    })
