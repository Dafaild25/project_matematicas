from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from ..models import Estudiantes, Modulos, Clases

# Create your views here.
@login_required 
def core_admin(request):
    total_estudiantes = Estudiantes.objects.count()
    total_modulos = Modulos.objects.count()
    total_clases = Clases.objects.count()

    contexto = {
        'total_estudiantes': total_estudiantes,
        'total_modulos': total_modulos,
        'total_clases': total_clases,
    }

    return render(request, 'core/index.html', contexto)