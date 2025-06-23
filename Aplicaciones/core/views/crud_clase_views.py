from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from ..models import Clases, Modulos, Docentes
from ..forms.clases_form import ClasesForm



def index(request):
    clases = Clases.objects.all()
    form = ClasesForm()
    docentes = Docentes.objects.filter(doc_estado=True)
    modulos = Modulos.objects.filter(mod_estado=True)
    clase_a_editar = None  # Para usar si queremos reabrir el modal con errores
    form_editar = None

    if request.method == 'POST':
        # Crear clase
        if 'crear_clase' in request.POST:
            form = ClasesForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Clase creada correctamente.')
                return redirect('clase_index')

        # Editar clase
        elif 'editar_clase' in request.POST:
            clase_id = request.POST.get('cla_id')
            print("🔧 Editando clase ID:", clase_id)  # debug
            clase = get_object_or_404(Clases, pk=clase_id)

            form_editar = ClasesForm(request.POST, instance=clase)
            form_editar.fields['fk_docente'].queryset = docentes
            form_editar.fields['fk_modulo'].queryset = modulos
            clase.cla_estado = 'cla_estado' in request.POST

            if form_editar.is_valid():
                form_editar.save()  # ✅ este es el correcto
                messages.success(request, f'Clase "{clase.cla_nombre}" actualizada correctamente.')
                return redirect('clase_index')
            else:
                messages.error(request, "❌ Error al editar la clase.")
                clase_a_editar = clase  # para abrir el modal y mostrar errores

        # Eliminar clase
        elif 'eliminar_clase' in request.POST:
            clase_id = request.POST.get('cla_id')
            clase = get_object_or_404(Clases, pk=clase_id)
            clase.cla_estado = False
            clase.save()
            messages.success(request, 'Clase eliminada correctamente.')
            return redirect('clase_index')

    return render(request, 'clases/Index.html', {
        'clases': clases,
        'form': form,
        'docentes': docentes,
        'modulos': modulos,
        'form_editar': form_editar,
        'clase_a_editar': clase_a_editar,
    })
        
    
    