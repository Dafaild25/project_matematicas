from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages  # Importar mensajes
from django.contrib.auth.models import Group # Importar grupos
from Aplicaciones.core.forms.user_form import UserForm  # Importar clase de registro
from ..models import * # Importar modelos
from Aplicaciones.core.validaciones.validar_cedula import * # Importar funciones de validaciones

# VISTA PRINCIPAL PARA LISTAR ESTUDIANTES
def index(request):
    estudiantes = Estudiantes.objects.all()  # Obtener todos los estudiantes
    return render(request, 'estudiante/index.html', {'estudiantes': estudiantes})

# VISTA PARA FORMULARIO ESTUDIANTE
def create_estudiante(request):
    return render(request, 'estudiante/Create.html')

# METODO CREAR UN NUEVO ESTUDIANTE
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
def actualizar_estudiante(request):
    if request.method == 'POST':
        try:
            # Obtener el ID del estudiante desde el formulario
            estud_id = request.POST['estud_id']
            estudiante = get_object_or_404(Estudiantes, pk=estud_id)  # Obtener el estudiante por su ID
            # Obtener los datos para tabla Estudiantes
            estudiante.est_fotografia = request.FILES.get('fotografia') if 'fotografia' in request.FILES else None
            estudiante.est_estado = request.POST['estado']
            estudiante.save()  # Actualizar los datos de Estudiantes
            # Obtener los datos para tabla Personas
            persona = estudiante.fk_id_persona  # Obtener la persona asociada al administrador
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
            return redirect('estudiante_index')
        
# METODO PARA ELIMINAR UN ESTUDIANTE
def eliminar_estudiante(request, id_estud):
    estudiante = get_object_or_404(Estudiantes, pk=id_estud)  # Obtener el estudiante por su ID
    try:
        estudiante.est_estado = False # Cambiar el estado a inactivo
        estudiante.save()  # Guardar los cambios
    except Exception as e:
        messages.error(request, f'Error al eliminar: {str(e)}')
    
    return redirect('estudiante_index')
