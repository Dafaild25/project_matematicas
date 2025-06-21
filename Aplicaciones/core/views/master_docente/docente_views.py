from django.shortcuts import render
from django.contrib.auth.models import User # Importar modelo User de Django
from ...models import *

# Create your views here.
def vista_docente(request):
    return render(request, 'masterdocente/index.html' );  