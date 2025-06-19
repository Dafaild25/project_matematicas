from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from ..models import Clases
from ..forms.clases_form import ClasesForm


def index(request):
    clases = Clases.objects.all()
    form = ClasesForm()
    if request.method == 'POST':
        form = ClasesForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Clase creada correctamente.')
            return redirect('clase_index')
    
    
    return render(request, 'clases/Index.html', {'clases': clases,'form': form})