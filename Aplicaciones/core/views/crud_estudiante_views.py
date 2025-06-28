from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages  # Importar mensajes
from django.contrib.auth.models import Group # Importar grupos
from Aplicaciones.core.forms.user_form import UserForm  # Importar clase de registro
from ..models import * # Importar modelos
from ..decorators import admin_required

# VISTA PRINCIPAL PARA LISTAR ESTUDIANTES

@admin_required
def index(request):
    # Obtener todos los estudiantes excluyendo al usuario logueado
    estudiantes = Estudiantes.objects.exclude(fk_id_persona__fk_id_usuario=request.user) 
    return render(request, 'estudiante/index.html', {'estudiantes': estudiantes})

# VISTA PARA FORMULARIO ESTUDIANTE
@admin_required
def create_estudiante(request):
    return render(request, 'estudiante/Create.html')

# METODO CREAR UN NUEVO ESTUDIANTE
@admin_required
def nuevo_estudiante(request):
    if(request.method == 'POST'):
        try:
            formUsuario = UserForm(request.POST) # Instanciar formulario de usuario
            # Campos del Auth_User
            nombre_grupo = 'Estudiantes' # Nombre del grupo
            grupo, created = Group.objects.get_or_create(name=nombre_grupo)
            usuario = formUsuario.save() # Guardar datos del User
            usuario.groups.add(grupo) # Agregar usuario al grupo
            #  Cambiar  a mayúsculas
            usuario.first_name = usuario.first_name.title() # Primera letra mayúscula
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

            # Campos de Estudiantes
            estudiante = Estudiantes.objects.create( # Crear registro de tabla Estudiantes
                fk_id_persona=persona,  # Relacionar con la persona creada
                est_fotografia= request.FILES.get('fotografia') if 'fotografia' in request.FILES else None,
            )
        except Exception as e:
            messages.error(request, f'Error al crear al estudiante: {str(e)}')
            print(f'Error al crear el estudiante: {str(e)}')
            return redirect('estudiante_create')  # Redirigir a la vista de creación si hay un error
    return redirect('estudiante_index')

# VISTA PARA EDITAR UN ESTUDIANTE
@admin_required
def edit_estudiante(request, id_estud):
    estudiante = get_object_or_404(Estudiantes,pk=id_estud) # Obtener el estudiante por su ID
    persona = estudiante.fk_id_persona # Obtener la persona asociada al estudiante
    usuario = persona.fk_id_usuario # Obtener el usuario asociado a la persona
    contexto = {
        'estudiante': estudiante,
        'persona': persona,
        'usuario': usuario
    }
    return render(request,'estudiante/Edit.html', contexto) # Renderizar la plantilla de edición

# METODO PARA ACTUALIZAR UN ESTUDIANTE
@admin_required
def actualizar_estudiante(request):
    if request.method == 'POST':
        try:
            # Obtener el ID del estudiante desde el formulario
            estud_id = request.POST['estud_id']
            estudiante = get_object_or_404(Estudiantes, pk=estud_id)  # Obtener el estudiante por su ID
            # Obtener los datos para tabla Estudiantes
            if 'fotografia' in request.FILES:
                estudiante.est_fotografia = request.FILES['fotografia']
            estudiante.est_estado = True if request.POST.get('estado') == 'True' else False
            estudiante.save()  # Actualizar los datos de Estudiantes
            # Obtener los datos para tabla Personas
            persona = estudiante.fk_id_persona  # Obtener la persona asociada al administrador
            persona.per_segundo_nombre = request.POST['segundo_nombre'].title() # Primera letra mayúscula
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
            return redirect('estudiante_index')
        
# METODO PARA ELIMINAR UN ESTUDIANTE
@admin_required
def eliminar_estudiante(request, id_estud):
    estudiante = get_object_or_404(Estudiantes, pk=id_estud)  # Obtener el estudiante por su ID
    try:
        estudiante.delete()  # Eliminar usuario
    except Exception as e:
        messages.error(request, f'Error al eliminar: {str(e)}')
    
    return redirect('estudiante_index')