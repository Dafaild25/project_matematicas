from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages  # Importar mensajes
from django.contrib.auth.models import Group # Importar grupos
from Aplicaciones.core.forms.user_form import *# Importar clase de validación de formularios
from ..models import * # Importar modelos
from ..decorators import admin_required  
from datetime import date # Importar fecha

# VISTA PRINCIPAL PARA LISTAR ADMINISTRADORES
@admin_required  # ← AGREGAR ESTE DECORADOR
def index(request):
    # Obtener todos los administradores excluyendo al usuario logueado
    administradores = Administradores.objects.exclude(fk_id_persona__fk_id_usuario=request.user) 
    return render(request, 'administrador/index.html', {'administradores': administradores})

# VISTA PARA FORMULARIO ADMINISTRADORES
@admin_required  # ← AGREGAR ESTE DECORADOR
def create_administrador(request):
    formUsuario = UserCreateForm()
    formPersona = PersonaCreateForm()
    return render(request, 'administrador/Create.html', {
        'formUsuario': formUsuario,
        'formPersona': formPersona
    })

# METODO CREAR UN NUEVO ADMINISTRADOR
@admin_required
def nuevo_administrador(request):
    formUsuario = UserCreateForm(request.POST or None) # Instanciar el formulario de usuario
    formPersona = PersonaCreateForm(request.POST or None) # Instanciar el formulario de persona
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
                messages.success(request, 'Administrador creado exitosamente.')
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
    # Crear los formularios precargados
    formUsuario = UserCreateForm(instance=usuario)
    initial_data = {
        'per_segundo_nombre': persona.per_segundo_nombre,
        'per_segundo_apellido': persona.per_segundo_apellido,
        'per_fecha_nacimiento': persona.per_fecha_nacimiento.strftime('%Y-%m-%d') if persona.per_fecha_nacimiento else '',
        'cedula': persona.per_cedula,
        'per_telefono': persona.per_telefono,
    }
    formPersona = PersonaCreateForm(initial=initial_data)
    contexto = {
        'formUsuario': formUsuario,
        'formPersona': formPersona,
        'administrador': administrador,
        'persona': persona,
    }
    return render(request, 'administrador/Edit.html', contexto)  # Renderizar la plantilla de edición

# METODO PARA ACTUALIZAR UN ADMINISTRADOR
@admin_required  # ← AGREGAR ESTE DECORADOR
def actualizar_administrador(request):
    if request.method == 'POST':
        # Obtener el ID del administrador desde el formulario
        admin_id = request.POST['admin_id']
        administrador = get_object_or_404(Administradores, pk=admin_id)  # Obtener el administrador por su ID
        persona = administrador.fk_id_persona  # Obtener la persona asociada al administrador
        usuario = persona.fk_id_usuario  # Obtener el usuario asociado a la persona
        # Instanciar el formulario de usuario con los datos del POST
        formUsuario = UserUpdateForm(request.POST, instance=usuario)
        # Instanciar el formulario de persona con los datos del POST
        formPersona = PersonaCreateForm(request.POST)
        # Validar cédula única excluyendo la actual
        cedula = request.POST.get('cedula').strip()
        if Personas.objects.filter(per_cedula=cedula).exclude(pk=persona.pk).exists():
            formPersona.add_error('cedula', 'Ya existe un usuario con este número de cédula.')
       # Validar formularios completos
        if not formUsuario.is_valid() or not formPersona.is_valid():
            messages.error(request, 'Hay errores en el formulario. Por favor revisa los campos resaltados.')
            print("Hay errores en el formulario. Por favor revisa los campos resaltados.: ",formUsuario.errors)
            return render(request, 'administrador/Edit.html', {
                'formUsuario': formUsuario,
                'formPersona': formPersona,
                'administrador': administrador,
                'persona': persona,
            })
        try:
            # Actualizar usuario
            usuario = formUsuario.save(commit=False)
            usuario.first_name = usuario.first_name.title()
            usuario.last_name = usuario.last_name.title()
            nueva_contrasena = request.POST.get('password')
            if nueva_contrasena:
                usuario.set_password(nueva_contrasena)
            usuario.save()
            # Obtener los datos para tabla Personas
            persona.per_segundo_nombre = formPersona.cleaned_data['per_segundo_nombre'].title()
            persona.per_segundo_apellido = formPersona.cleaned_data['per_segundo_apellido'].title()
            persona.per_fecha_nacimiento = formPersona.cleaned_data['per_fecha_nacimiento']
            persona.per_cedula = cedula
            persona.per_telefono = formPersona.cleaned_data['per_telefono']
            persona.save()
            # Obtener los datos para tablaAdministradores
            if 'fotografia' in request.FILES:
                administrador.adm_fotografia = request.FILES['fotografia']           
            administrador.adm_estado = True if request.POST.get('estado') == 'True' else False
            administrador.save()  # Actualizar los datos de Administradores
            messages.success(request, 'Administrador actualizado exitosamente.')
            return redirect('administrador_index')
        except Exception as e:
                messages.error(request, f'Error al actualizar el administrador: {str(e)}')
        return render(request, 'administrador/Edit.html', {
            'formUsuario': formUsuario,
            'formPersona': formPersona,
            'administrador': administrador,
            'persona': persona,
        })

@admin_required  
def eliminar_administardor(request, id_admin):
    admin = get_object_or_404(Administradores, pk=id_admin)  # Obtener el administrador por su ID
    try:
        admin.delete()  # Eliminar usuario
    except Exception as e:
        messages.error(request, f'Error al eliminar: {str(e)}')
    
    return redirect('administrador_index')