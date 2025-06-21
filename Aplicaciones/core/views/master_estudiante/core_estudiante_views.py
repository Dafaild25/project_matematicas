from django.shortcuts import render
from django.contrib.auth.models import User # Importar modelo User de Django
from ...models import *

# Create your views here.
def core_estudiante(request):
    return render(request, 'masterestudiante/core/Index.html' );  