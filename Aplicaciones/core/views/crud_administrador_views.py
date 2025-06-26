from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages  # Importar mensajes
from django.contrib.auth.models import Group # Importar grupos
from Aplicaciones.core.forms.user_form import UserForm # Importar clase de registro
from ..models import * # Importar modelos
from Aplicaciones.core.validaciones.validar_cedula import * # Importar funciones de validaciones
from Aplicaciones.core.decorators import rol_required # Importar decorador para requerir administrador

# VISTA PRINCIPAL PARA LISTAR ADMINISTRADORES
@rol_required('administrador')
def index(request):
    # Obtener todos los administradores excluyendo al usuario logueado
    administradores = Administradores.objects.exclude(fk_id_persona__fk_id_usuario=request.user) 
    return render(request, 'administrador/index.html', {'administradores': administradores})

# VISTA PARA FORMULARIO ADMINISTRADORES
@rol_required('administrador')
def create_administrador(request):
    return render(request, 'administrador/Create.html')

# METODO CREAR UN NUEVO ADMINISTRADOR
@rol_required('administrador')
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
            usuario.first_name = usuario.first_name.title()  # Primera letra mayúscula
            usuario.last_name = usuario.last_name.title()       
            usuario.save()  # Guardar los cambios

            # Campos de Personas
            persona = Personas.objects.create(# Crear  registro de tabla Personas
                fk_id_usuario=usuario,  # Relacionar con el usuario creado
                per_segundo_nombre = request.POST['segundo_nombre'].title(),
                per_segundo_apellido = request.POST['segundo_apellido'].title(),
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
@rol_required('administrador')
def edit_administrador(request, id_admin):
    administrador = get_object_or_404(Administradores,pk=id_admin)  # Obtener el administrador por su ID
    persona = administrador.fk_id_persona  # Obtener la persona asociada al administrador
    usuario = persona.fk_id_usuario  # Obtener el usuario asociado a la persona
    contexto = {
        'admin': administrador,
        'persona': persona,
        'usuario': usuario,
    }
    return render(request, 'administrador/Edit.html', contexto)  # Renderizar la plantilla de edición

# METODO PARA ACTUALIZAR UN ADMINISTRADOR
@rol_required('administrador')
def actualizar_administrador(request):
    if request.method == 'POST':
        try:
            # Obtener el ID del administrador desde el formulario
            admin_id = request.POST['admin_id']
            administrador = get_object_or_404(Administradores, pk=admin_id)  # Obtener el administrador por su ID
            # Obtener los datos para tabla Administradores
            if 'fotografia' in request.FILES:
                administrador.adm_fotografia = request.FILES['fotografia']           
            administrador.adm_estado = True if request.POST.get('estado') == 'True' else False
            administrador.save()  # Actualizar los datos de Administradores
            # Obtener los datos para tabla Personas
            persona = administrador.fk_id_persona  # Obtener la persona asociada al administrador
            persona.per_segundo_nombre = request.POST['segundo_nombre'].title() # Cambiar a mayúsculas
            persona.per_segundo_apellido = request.POST['segundo_apellido'].title() 
            persona.per_fecha_nacimiento = request.POST['fecha_nacimiento']
            persona.per_cedula = request.POST['cedula']
            persona.per_telefono = request.POST['telefono']
            persona.save()  # Actualizar los datos de Personas

            # Obtener los datos para tabla User
            usuario = persona.fk_id_usuario  # Obtener el usuario asociado a la persona
            formUsuario = UserForm(request.POST, instance=usuario)  # Instanciar formulario
            if formUsuario.is_valid(): # Validar el formulario
                usuario.first_name = usuario.first_name.title() 
                usuario.last_name = usuario.last_name.title() 
                # Validar si se quiere cambiar la contraseña
                nueva_contrasena = request.POST.get('password')
                if nueva_contrasena:
                    usuario.set_password(nueva_contrasena)
                usuario = formUsuario.save()
            else:
                print("Formulario de usuario no válido:", formUsuario.errors)
        except KeyError:
            print("Error al obtener los datos del formulario")
        finally:
            return redirect('administrador_index')

# METODO PARA ELIMINAR UN ADMINISTRADOR
@rol_required('administrador')
def eliminar_administardor(request, id_admin):
    admin = get_object_or_404(Administradores, pk=id_admin)  # Obtener el administrador por su ID
    try:
        admin.delete()  # Eliminar usuario
    except Exception as e:
        messages.error(request, f'Error al eliminar: {str(e)}')
    
    return redirect('administrador_index')