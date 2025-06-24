from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.cache import never_cache # Importar decorador para evitar caché
from django.contrib import messages  # Importar mensajes
from django.contrib.auth.models import Group # Importar grupos
from Aplicaciones.core.forms.user_form import UserForm # Importar clase de registro
from ..models import * # Importar modelos
from Aplicaciones.core.validaciones.validar_cedula import * # Importar funciones de validaciones


# VISTA PRINCIPAL PARA LISTAR DOCENTES
def index(request):
    docentes = Docentes.objects.all()  # Obtener todos los docentes
    return render(request, 'docente/index.html', {'docentes': docentes})

# VISTA PARA FORMULARIO DOCENTES
def create_docente(request):
    return render(request, 'docente/Create.html')

# METODO CREAR UN NUEVO DOCENTE
def nuevo_docente(request):
    if(request.method == 'POST'):
        try:
            formUsuario = UserForm(request.POST) # Instanciar formulario de usuario
            # Campos del Auth_User
            nombre_grupo = 'Docentes' # Nombre del grupo
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

            # Campos de Docentes
            docente = Docentes.objects.create( # Crear registro de tabla Docentes
                fk_id_persona=persona,  # Relacionar con la persona creada
                doc_fotografia= request.FILES.get('fotografia') if 'fotografia' in request.FILES else None,
            )
        except Exception as e:
            messages.error(request, f'Error al crear al docente: {str(e)}')
            print(f'Error al crear el docente: {str(e)}')
            return redirect('docente_create')  # Redirigir a la vista de creación si hay un error
    return redirect('docente_index')

# VISTA PARA EDITAR UN DOCENTE
def edit_docente(request, id_docen):
    docente = get_object_or_404(Docentes,pk=id_docen) # Obtener el docente por su ID
    persona = docente.fk_id_persona # Obtener la persona asociada al docente
    usuario = persona.fk_id_usuario # Obtener el usuario asociado a la persona
    contexto = {
        'docente': docente,
        'persona': persona,
        'usuario': usuario
    }
    return render(request,'docente/Edit.html', contexto) # Renderizar la plantilla de edición

# METODO PARA ACTUALIZAR UN DOCENTE
def actualizar_docente(request):
    if request.method == 'POST':
        try:
            # Obtener el ID del docente desde el formulario
            docen_id = request.POST['docen_id']
            docente = get_object_or_404(Docentes, pk=docen_id)  # Obtener el docente por su ID
            # Obtener los datos para tabla Docentes
            docente.doc_fotografia = request.FILES.get('fotografia') if 'fotografia' in request.FILES else None
            docente.doc_estado = request.POST['estado']
            docente.save()  # Actualizar los datos de Docentes
            # Obtener los datos para tabla Personas
            persona = docente.fk_id_persona  # Obtener la persona asociada al administrador
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
            return redirect('docente_index')
        
# METODO PARA ELIMINAR UN DOCENTE
def eliminar_docente(request, id_docen):
    docente = get_object_or_404(Docentes, pk=id_docen)  # Obtener el docente por su ID
    try:
        docente.doc_estado = False # Cambiar el estado a inactivo
        docente.save()  # Guardar los cambios
    except Exception as e:
        messages.error(request, f'Error al eliminar: {str(e)}')
    
    return redirect('docente_index')
