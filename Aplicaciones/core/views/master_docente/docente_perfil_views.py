from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages  # Importar mensajes
from Aplicaciones.core.forms.user_form import *  # Importar clase de registro
from ...models import * # Importar modelos
from ...decorators import docente_required # Importar decorador de permisos

# VISTA EDITAR PERFIL DEL DOCENTE
@docente_required
def editar_perfil_docente(request):
    # Obtener el docente que corresponde al usuario logueado
    docente = get_object_or_404(Docentes, fk_id_persona__fk_id_usuario=request.user)
    persona = docente.fk_id_persona # Obtener la persona asociada al estudiante
    usuario = persona.fk_id_usuario # Obtener el usuario asociado a la persona
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
        'docente': docente,
        'persona': persona,
    }
    return render(request, 'masterdocente/perfil/Edit.html', contexto)

# METODO PARA ACTUALIZAR EL PERFIL DEL DOCENTE
@docente_required
def actualizar_perfil_docente(request):
    if request.method == 'POST':
        # Obtener el estudiante que corresponde al usuario logueado
        docente = get_object_or_404(Docentes, fk_id_persona__fk_id_usuario=request.user)
        persona = docente.fk_id_persona  # Obtener la persona asociada al administrador
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
            return render(request, 'masterdocente/perfil/Edit.html', {
                'formUsuario': formUsuario,
                'formPersona': formPersona,
                'docente': docente,
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
            # Obtener los datos para tabla Estudiantes
            if 'fotografia' in request.FILES:
                docente.doc_fotografia = request.FILES['fotografia']
            docente.save()  # Actualizar los datos de Docentes
            messages.success(request, 'Docente actualizado exitosamente.')
            return redirect('core_docente')
        except Exception as e:
                messages.error(request, f'Error al actualizar el docente: {str(e)}')
        return render(request, 'masterdocente/perfil/Edit.html', {
            'formUsuario': formUsuario,
            'formPersona': formPersona,
            'docente': docente,
            'persona': persona,
        })