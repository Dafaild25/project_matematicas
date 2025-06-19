from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from ..models import Niveles,Modulos
from ..forms.niveles_form import NivelesForm
from ..utils.nivel_utils import tiene_dependencias_nivel

def index(request):
    niveles = Niveles.objects.filter(niv_estado=True)
    form = NivelesForm()
    form_editar = None
    nivel_a_editar = None

    if request.method == 'POST':
        # CREAR
        if 'crear_nivel' in request.POST:
            form = NivelesForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Nivel creado correctamente.')
                return redirect('nivel_index')

        # EDITAR
        elif 'editar_nivel' in request.POST:
            nivel_id = request.POST.get('niv_id')
            
            nivel = get_object_or_404(Niveles, pk=nivel_id)
            form_editar = NivelesForm(request.POST, instance=nivel)
            form_editar.fields['fk_modulo'].queryset = Modulos.objects.all()
            if form_editar.is_valid():
                form_editar.save()
                messages.success(request, f'Nivel "{nivel.niv_nombre}" actualizado correctamente.')
                return redirect('nivel_index')
            else:
                
                nivel_a_editar = nivel  # para volver a abrir el modal

        # ELIMINAR (borrado lógico)
        elif 'eliminar_nivel' in request.POST:
            nivel_id = request.POST.get('niv_id')
            nivel = get_object_or_404(Niveles, pk=nivel_id)

            if not tiene_dependencias_nivel(nivel):
                nivel.niv_estado = False
                nivel.save()
                messages.success(request, f'Nivel "{nivel.niv_nombre}" eliminado correctamente.')
            else:
                messages.error(request, f'No se puede eliminar el nivel "{nivel.niv_nombre}" porque tiene dependencias.')

            return redirect('nivel_index')

    return render(request, 'nivel/index.html', {
        'niveles': niveles,
        'form': form,
        'form_editar': form_editar,
        'nivel_a_editar': nivel_a_editar
    })
