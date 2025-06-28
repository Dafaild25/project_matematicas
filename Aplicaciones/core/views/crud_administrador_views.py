from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages  # Importar mensajes
from django.contrib.auth.models import Group # Importar grupos
from Aplicaciones.core.forms.user_form import UserForm, PersonaForm # Importar clase de validación de formularios
from ..models import * # Importar modelos
from ..decorators import admin_required  

# VISTA PRINCIPAL PARA LISTAR ADMINISTRADORES
@admin_required  # ← AGREGAR ESTE DECORADOR
def index(request):
    # Obtener todos los administradores excluyendo al usuario logueado
    administradores = Administradores.objects.exclude(fk_id_persona__fk_id_usuario=request.user) 
    return render(request, 'administrador/index.html', {'administradores': administradores})

# VISTA PARA FORMULARIO ADMINISTRADORES
@admin_required  # ← AGREGAR ESTE DECORADOR
def create_administrador(request):
    formUsuario = UserForm()
    formPersona = PersonaForm()
    return render(request, 'administrador/Create.html', {
        'formUsuario': formUsuario,
        'formPersona': formPersona
    })

# METODO CREAR UN NUEVO ADMINISTRADOR
@admin_required
def nuevo_administrador(request):
    formUsuario = UserForm(request.POST or None) # Instanciar el formulario de usuario
    formPersona = PersonaForm(request.POST or None) # Instanciar el formulario de persona
    if request.method == 'POST':
        cedula = request.POST.get('cedula', '').strip() # Obtener cedula del formulario
        cedula_existente = Personas.objects.filter(per_cedula=cedula).exists() # Verificar si existe la cedula
        if cedula_existente:
            formPersona.add_error('cedula', 'La cédula ya está registrada.') # Agregar error al formulario si la cedula ya existe
        if formUsuario.is_valid() and formPersona.is_valid():
            try:
                nombre_grupo = 'Administradores'
                grupo, created = Group.objects.get_or_create(name=nombre_grupo)
                usuario = formUsuario.save() # Guardar el usuario
                usuario.first_name = usuario.first_name.title()
                usuario.last_name = usuario.last_name.title()
                usuario.save() # Guardar el usuario con los cambios
                usuario.groups.add(grupo) # Agregar el grupo al usuario
                # Datos para la tabla Personas
                persona = Personas.objects.create(
                    fk_id_usuario=usuario,
                    per_segundo_nombre=request.POST.get('per_segundo_nombre', '').title(),
                    per_segundo_apellido=request.POST.get('per_segundo_apellido', '').title(),
                    per_fecha_nacimiento=request.POST.get('per_fecha_nacimiento'),
                    per_cedula=request.POST.get('cedula'),
                    per_telefono=request.POST.get('per_telefono', '')
                )
                # Datos para la tabla Administradores
                Administradores.objects.create(
                    fk_id_persona=persona,
                    adm_fotografia=request.FILES.get('fotografia') if 'fotografia' in request.FILES else None
                )
                messages.success(request, 'Administrador creado correctamente.')
                return redirect('administrador_index')
            except Exception as e:
                messages.error(request, f'Error al crear el administrador: {str(e)}')
                # Si ocurre un error, se renderiza de nuevo el formulario con los datos ingresados
                return render(request, 'administrador/Create.html', {
                    'formUsuario': formUsuario,
                    'formPersona': formPersona
                })
    # Si el formulario no es válido, se renderiza de nuevo con los errores
    return render(request, 'administrador/Create.html', {
        'formUsuario': formUsuario,
        'formPersona': formPersona
    })

# VISTA PARA EDITAR UN ADMINISTRADOR
@admin_required  # ← AGREGAR ESTE DECORADOR
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
@admin_required  # ← AGREGAR ESTE DECORADOR
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


@admin_required  
def eliminar_administardor(request, id_admin):
    admin = get_object_or_404(Administradores, pk=id_admin)  # Obtener el administrador por su ID
    try:
        admin.delete()  # Eliminar usuario
    except Exception as e:
        messages.error(request, f'Error al eliminar: {str(e)}')
    
    return redirect('administrador_index')