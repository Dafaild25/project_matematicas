from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import Group # Importar grupos
from Aplicaciones.core.forms import * # Importar clase de registro
from ..models import * # Importar modelos


def index(request):
    administradores = Administradores.objects.all()  # Obtener todos los administradores
    return render(request, 'administrador/index.html', {'administradores': administradores})

# VISTA PARA ADMINISTRADORES
def create(request):
    return render(request, 'administrador/Create.html')

# METODO CREAR UN NUEVO ADMINISTRADOR
def nuevo_administrador(request):
    if(request.method == 'POST'):
        formUsuario = UserForm(request.POST) # Instanciar formulario de usuario
        # Campos del Auth_User
        nombre_grupo = 'Administradores' # Nombre del grupo
        grupo, created = Group.objects.get_or_create(name=nombre_grupo)
        usuario = formUsuario.save() # Guardar datos del User
        usuario.groups.add(grupo) # Agregar usuario al grupo
        #  Cambiar  a mayúsculas
        usuario.first_name = usuario.first_name.upper()
        usuario.last_name = usuario.last_name.upper()         
        usuario.save()  # Guardar los cambios

        # Campos de Personas
        segundo_nombre = request.POST['segundo_nombre'].upper()
        segundo_apellido = request.POST['segundo_apellido'].upper()
        fecha_nacimiento = request.POST['fecha_nacimiento']
        cedula = request.POST['cedula']
        telefono = request.POST['telefono']
        personas = Personas(
            fk_id_usuario=usuario,  # Relacionar con el usuario creado
            per_segundo_nombre=segundo_nombre,
            per_segundo_apellido=segundo_apellido,
            per_fecha_nacimiento=fecha_nacimiento,
            per_cedula=cedula,
            per_telefono=telefono
        )
        personas.save() # Guardar los cambios

        # Campos de Administradores
        fotografia = request.FILES.get('fotografia') if 'fotografia' in request.FILES else None
        admin = Administradores(
            fk_id_persona=personas,  # Relacionar con la persona creada
            adm_fotografia=fotografia
        )
        admin.save()

    return render(request, 'administrador/index.html')

# VISTA PARA EDITAR UN ADMINISTRADOR
def edit(request, id_admin):
    administrador = get_object_or_404(Administradores,pk=id_admin)  # Obtener el administrador por su ID
    persona = administrador.fk_id_persona  # Obtener la persona asociada al administrador
    return render(request, 'administrador/Edit.html', {'administrador': administrador})

# METODO PARA ACTUALIZAR UN ADMINISTRADOR
def actualizar_administrador(request):
    if request.method == 'POST':
        admin_id = request.POST['admin_id']  # Obtener el ID del administrador desde el formulario
        print("ID: ",admin_id)  # Imprimir el ID del administrador para depuración
        administrador = get_object_or_404(Administradores, pk=admin_id)  # Obtener el administrador por su ID
        print(administrador)  # Imprimir el administrador para depuración
        persona = administrador.fk_id_persona  # Obtener la persona asociada al administrador
        print(persona)  # Imprimir la persona para depuración
        usuario = persona.fk_id_usuario
        print(usuario)
        # Instanciar formulario de usuario con datos existentes
        formUsuario = UserForm(request.POST, instance=usuario)
        if formUsuario.is_valid():
            usuario.first_name = usuario.first_name.upper()
            usuario.last_name = usuario.last_name.upper()      
            usuario = formUsuario.save()  # Guardar los cambios en el usuario
            # Actualizar campos de Personas
            persona.per_segundo_nombre = request.POST['segundo_nombre'].upper()
            persona.per_segundo_apellido = request.POST['segundo_apellido'].upper()
            persona.per_fecha_nacimiento = request.POST['fecha_nacimiento']
            persona.per_cedula = request.POST['cedula']
            persona.per_telefono = request.POST['telefono']
            persona.save()  # Guardar los cambios en la persona

            # Actualizar campos de Administradores
            fotografia = request.FILES.get('fotografia') if 'fotografia' in request.FILES else None
            administrador.adm_fotografia = fotografia
            administrador.save()  # Guardar los cambios en el administrador

    return redirect('administrador_index')  # Redirigir a la lista de administradores

# METODO PARA ELIMINAR UN ADMINISTRADOR
