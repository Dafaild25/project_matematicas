from django.shortcuts import render, redirect, get_object_or_404
from django.forms import modelformset_factory
from django.contrib import messages
from ..models import Enunciados, Preguntas, Opciones, Modulos, Niveles
from ..forms.enunciado_form import EnunciadoForm, PreguntaFormSet, OpcionFormSet
from django.db import transaction
from django.http import JsonResponse



def index(request):
    buscar = request.GET.get("buscar", "").strip()
    modulo_id = request.GET.get("modulo")

    enunciados = Enunciados.objects.filter(enun_estado=True).select_related('fk_nivel', 'fk_nivel__fk_modulo').prefetch_related('preguntas_set__opciones_set')

    if buscar:
        enunciados = enunciados.filter(enun_nombre__icontains=buscar)

    if modulo_id:
        enunciados = enunciados.filter(fk_nivel__fk_modulo__id=modulo_id)

    enunciados = enunciados.select_related('fk_nivel', 'fk_nivel__fk_modulo').prefetch_related('preguntas_set', 'preguntas_set__opciones_set')

    modulos = Modulos.objects.all()

    return render(request, 'enunciado/index.html', {
        'enunciados': enunciados,
        'modulos': modulos,
    })



def create(request):
    if request.method == 'POST':
        print("📥 POST recibido")
        print("🔎 POST fk_nivel:", request.POST.get("fk_nivel"))
        form_enunciado = EnunciadoForm(data=request.POST)
        formset_preguntas = PreguntaFormSet(request.POST, request.FILES, prefix='pregunta')

        print("✅ Enunciado válido:", form_enunciado.is_valid())
        print("✅ Preguntas válidas:", formset_preguntas.is_valid())

        if form_enunciado.is_valid() and formset_preguntas.is_valid():
            try:
                with transaction.atomic():
                    enunciado = form_enunciado.save(commit=False)
                    enunciado.fk_nivel = form_enunciado.cleaned_data['fk_nivel']
                    enunciado.save()
                    print("📌 Enunciado creado:", enunciado)

                    preguntas = formset_preguntas.save(commit=False)
                    for index, pregunta in enumerate(preguntas):
                        pregunta.fk_enunciado = enunciado
                        pregunta.save()
                        print(f"✅ Pregunta #{index+1} guardada:", pregunta)

                        total_opciones = 0
                        while True:
                            nombre_key = f'opciones-{index}-{total_opciones}-op_nombre'
                            correcta_key = f'opciones-{index}-{total_opciones}-op_correcta'
                            if nombre_key not in request.POST:
                                break
                            texto = request.POST.get(nombre_key)
                            correcta = request.POST.get(correcta_key) == 'on'
                            if texto:
                                Opciones.objects.create(
                                    fk_pregunta=pregunta,
                                    op_nombre=texto,
                                    op_correcta=correcta
                                )
                            total_opciones += 1

                    messages.success(request, 'El enunciado y sus preguntas se guardaron correctamente.')
                    return redirect('enunciado_index')
            except Exception as e:
                print("❌ Error al guardar:", e)
                messages.error(request, f'Ocurrió un error: {str(e)}')
        else:
            print("❌ Formulario no válido")
            print("Errores en EnunciadoForm:", form_enunciado.errors.as_data())
            print("Errores en Preguntas:", formset_preguntas.errors)
            messages.error(request, 'Revisa los campos del formulario.')
    else:
        form_enunciado = EnunciadoForm()
        formset_preguntas = PreguntaFormSet(prefix='pregunta')

    return render(request, 'enunciado/Create.html', {
        'form_enunciado': form_enunciado,
        'formset_preguntas': formset_preguntas
    })




def cargar_niveles(request):
    modulo_id = request.GET.get('modulo_id')
    niveles = Niveles.objects.filter(fk_modulo=modulo_id).values('niv_id', 'niv_nombre')

    return JsonResponse(list(niveles), safe=False)

 
    
def editar(request, enun_id):
    enunciado = get_object_or_404(Enunciados, pk=enun_id, enun_estado=True)
    preguntas_existentes = Preguntas.objects.filter(fk_enunciado=enunciado)

    if request.method == 'POST':
        form_enunciado = EnunciadoForm(request.POST, instance=enunciado)
        formset_preguntas = PreguntaFormSet(request.POST, request.FILES, instance=enunciado, prefix='pregunta')

        if form_enunciado.is_valid() and formset_preguntas.is_valid():
            try:
                with transaction.atomic():
                    form_enunciado.save()
                    formset_preguntas.save()
                    messages.success(request, 'El enunciado fue actualizado correctamente.')
                    return redirect('enunciado_index')
            except Exception as e:
                messages.error(request, f'Ocurrió un error al actualizar: {e}')
        else:
            messages.error(request, 'Corrige los errores del formulario.')
    else:
        form_enunciado = EnunciadoForm(instance=enunciado)
        formset_preguntas = PreguntaFormSet(instance=enunciado, prefix='pregunta')

    return render(request, 'enunciado/Edit.html', {
        'form_enunciado': form_enunciado,
        'formset_preguntas': formset_preguntas,
        'enunciado': enunciado,
    })


def eliminar(request, enun_id):
    enunciado = get_object_or_404(Enunciados, pk=enun_id, enun_estado=True)

    if request.method == 'POST':
        if enunciado.preguntas_set.exists():
            messages.error(request, "No se puede eliminar el enunciado porque tiene preguntas asociadas.")
        else:
            enunciado.enun_estado = False
            enunciado.save()
            messages.success(request, 'Enunciado eliminado correctamente.')
        return redirect('enunciado_index')

    return redirect('enunciado_index')
