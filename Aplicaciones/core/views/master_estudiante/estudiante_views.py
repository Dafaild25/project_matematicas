from django.shortcuts import render
from django.contrib.auth.models import User # Importar modelo User de Django
from ...models import *

# Create your views here.
def vista_estudiante(request):
    return render(request, 'masterestudiante/index.html' );  