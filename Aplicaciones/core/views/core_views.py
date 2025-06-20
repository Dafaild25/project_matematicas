from django.shortcuts import render
from ..models import Estudiantes, Modulos, Clases

# Create your views here.

def inicio(request):
    total_estudiantes = Estudiantes.objects.count()
    total_modulos = Modulos.objects.count()
    total_clases = Clases.objects.count()

    contexto = {
        'total_estudiantes': total_estudiantes,
        'total_modulos': total_modulos,
        'total_clases': total_clases,
    }

    return render(request, 'core/index.html', contexto)