from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages  # Importar mensajes
from django.contrib.auth.models import Group # Importar grupos
from Aplicaciones.core.forms import * # Importar clase de registro
from ..models import * # Importar modelos
from Aplicaciones.core.validaciones.validar_cedula import * # Importar funciones de validaciones


def index(request):
    administradores = Administradores.objects.all()  # Obtener todos los administradores
    return render(request, 'administrador/index.html', {'administradores': administradores})

# VISTA PARA ADMINISTRADORES
def create(request):
    return render(request, 'administrador/Create.html')

# METODO CREAR UN NUEVO ADMINISTRADOR
def nuevo_administrador(request):
    if(request.method == 'POST'):
        try:
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
            persona = Personas.objects.create(# Crear  registro de tabla Personas
                fk_id_usuario=usuario,  # Relacionar con el usuario creado
                per_segundo_nombre = request.POST['segundo_nombre'].upper(),
                per_segundo_apellido = request.POST['segundo_apellido'].upper(),
                per_fecha_nacimiento = request.POST['fecha_nacimiento'],
                per_cedula = request.POST['cedula'],
                per_telefono = request.POST['telefono']
            )

            # Campos de Administradores
            admin = Administradores.objects.create( # Crear registro de tabla Administradores
                fk_id_persona=persona,  # Relacionar con la persona creada
                adm_fotografia= request.FILES.get('fotografia') if 'fotografia' in request.FILES else None,
            )
        except Exception as e:
            messages.error(request, f'Error al crear el administrador: {str(e)}')
            print(f'Error al crear el administrador: {str(e)}')
            return redirect('administrador_create')  # Redirigir a la vista de creación si hay un error
    return redirect('administrador_index')

# VISTA PARA EDITAR UN ADMINISTRADOR
def edit(request, id_admin):
    administrador = get_object_or_404(Administradores,pk=id_admin)  # Obtener el administrador por su ID
    persona = administrador.fk_id_persona  # Obtener la persona asociada al administrador
    usuario = persona.fk_id_usuario  # Obtener el usuario asociado a la persona
    contexto = {
        'admin': administrador,
        'persona': persona,
        'usuario': usuario,
    }
    return render(request, 'administrador/Edit.html', contexto)  # Renderizar la plantilla de edición con el contexto

# METODO PARA ACTUALIZAR UN ADMINISTRADOR
def actualizar_administrador(request):
    if request.method == 'POST':
        try:
            # Obtener el ID del administrador desde el formulario
            admin_id = request.POST['admin_id']
            administrador = get_object_or_404(Administradores, pk=admin_id)  # Obtener el administrador por su ID
            # Obtener los datos para tabla Administradores
            administrador.adm_fotografia = request.FILES.get('fotografia') if 'fotografia' in request.FILES else None
            administrador.adm_estado = request.POST['estado']
            administrador.save()  # Actualizar los datos de Administradores
            # Obtener los datos para tabla Personas
            persona = administrador.fk_id_persona  # Obtener la persona asociada al administrador
            persona.per_segundo_nombre = request.POST['segundo_nombre'].upper()
            persona.per_segundo_apellido = request.POST['segundo_apellido'].upper()
            persona.per_fecha_nacimiento = request.POST['fecha_nacimiento']
            persona.per_cedula = request.POST['cedula']
            persona.per_telefono = request.POST['telefono']
            persona.save()  # Actualizar los datos de Personas

            # Obtener los datos para tabla User
            usuario = persona.fk_id_usuario  # Obtener el usuario asociado a la persona
            formUsuario = UserForm(request.POST, instance=usuario)  # Instanciar formulario
            if formUsuario.is_valid(): # Validar el formulario
                usuario.first_name = usuario.first_name.upper()
                usuario.last_name = usuario.last_name.upper()      
                usuario = formUsuario.save()
            else:
                print("Formulario de usuario no válido:", formUsuario.errors)
        except KeyError:
            print("Error al obtener los datos del formulario")
        finally:
            return redirect('administrador_index')

# METODO PARA ELIMINAR UN ADMINISTRADOR
def eliminar_administardor(request, id_admin):
    print(id_admin)
    admin = get_object_or_404(Administradores, pk=id_admin)  # Obtener el administrador por su ID
    try:
        print(admin)
        admin.adm_estado = False  # Cambiar el estado a inactivo
        admin.save()  # Guardar los cambios
    except Exception as e:
        messages.error(request, f'Error al eliminar: {str(e)}')
    
    return redirect('administrador_index')
