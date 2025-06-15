from django.db import transaction
from django.shortcuts import render, redirect
from ..models import Persona, Usuario, Administrador

def index(request):
    return render(request, 'administrador/index.html')

def create(request):
    return render(request, 'administrador/create.html')

@transaction.atomic
def crear_administrador(request):
    if request.method == 'POST':
        try:
            # Paso 1: Crear Persona
            persona = Persona.objects.create(
                nombres=request.POST['nombres'],
                apellidos=request.POST['apellidos'],
                dni=request.POST['dni'] == 'true',
                email=request.POST['email']
            )

            # Paso 2: Crear Usuario
            usuario = Usuario.objects.create(
                username=request.POST['username'],
                password=request.POST['password'],  # ⚠️ Codifica si es sensible
                persona=persona,
                estado='activo'
            )

            # Paso 3: Crear Administrador
            Administrador.objects.create(
                usuario=usuario
            )

            return redirect('lista_administradores')  # o render de éxito
        except Exception as e:
            transaction.set_rollback(True)
            return render(request, 'page/Page_404.html', {'error': str(e)})

    return render(request, 'core/crear_administrador.html')
