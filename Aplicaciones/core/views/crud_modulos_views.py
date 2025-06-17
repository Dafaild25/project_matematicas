from django.shortcuts import render, redirect, get_object_or_404
from ..models import Modulos
from ..forms.modulos_form import ModulosForm
from ..utils.Modulo_Utils import tiene_dependencias
from django.contrib import messages


def index(request):
    modulos = Modulos.objects.all()
    form = ModulosForm()
    form_editar = None
    modulo_a_editar = None

    if request.method == 'POST':
        # CREAR
        if 'crear_modulo' in request.POST:
            form = ModulosForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Módulo creado correctamente.')
                return redirect('modulo_index')

        # EDITAR
        elif 'editar_modulo' in request.POST:
            mod_id = request.POST.get('mod_id')
            modulo = get_object_or_404(Modulos, pk=mod_id)
            form_editar = ModulosForm(request.POST, instance=modulo)
            if form_editar.is_valid():
                form_editar.save()
                messages.success(request, f'Módulo "{modulo.mod_nombre}" actualizado correctamente.')
                return redirect('modulo_index')
            else:
                modulo_a_editar = modulo  # para volver a abrir el modal

        # ELIMINAR (borrado lógico)
        elif 'eliminar_modulo' in request.POST:
            mod_id = request.POST.get('mod_id')
            modulo = get_object_or_404(Modulos, pk=mod_id)

            if not tiene_dependencias(modulo):
                modulo.delete()
                messages.success(request, f'Módulo "{modulo.mod_nombre}" eliminado correctamente.')
            else:
                messages.error(
                    request,
                    f'No se puede eliminar el módulo "{modulo.mod_nombre}" porque tiene dependencias.'
                )

            return redirect('modulo_index')

    return render(request, 'modulo/index.html', {
        'modulos': modulos,
        'form': form,
        'form_editar': form_editar,
        'modulo_a_editar': modulo_a_editar
    })



