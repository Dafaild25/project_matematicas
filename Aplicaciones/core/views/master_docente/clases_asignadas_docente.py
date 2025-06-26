from django.shortcuts import render, get_object_or_404,redirect
from django.db.models import Count
from ...models import Clases, Estudiantes, Docentes, Matriculas, Personas,Niveles,User,Avance_Matriculados
from django.http import HttpResponseForbidden, JsonResponse
from ...forms.docente_estudiante_form import CrearEstudianteForm
from django.db import transaction
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.contrib.auth.models import Group
from django.views.decorators.http import require_GET, require_POST
import pandas as pd
from django.views.decorators.csrf import csrf_exempt
from Aplicaciones.core.decorators import rol_required # Importar decorador para requerir docente

@rol_required('docente')
def clases_asignadas_docente(request):
    # Obtener la persona vinculada al usuario logueado
    persona = get_object_or_404(Personas, fk_id_usuario=request.user)

    # Obtener el docente correspondiente
    docente = get_object_or_404(Docentes, fk_id_persona=persona)

    # Obtener las clases asignadas al docente
    clases = Clases.objects.filter(fk_docente=docente) \
        .annotate(num_matriculados=Count('matriculas'))

    return render(request, 'masterdocente/clase/Clase_Asignada.html', {
        'clases': clases
    })
    
    
    
@rol_required('docente')
def matriculados_asignados_docente(request, clase_id):
    # Obtener la persona vinculada al usuario logueado
    persona = get_object_or_404(Personas, fk_id_usuario=request.user)

    # Obtener el docente correspondiente
    docente = get_object_or_404(Docentes, fk_id_persona=persona)

    # Obtener la clase específica
    clase = get_object_or_404(Clases, pk=clase_id, fk_docente=docente)

    # Estudiantes matriculados en esa clase
    matriculas = Matriculas.objects.filter(fk_clase=clase).select_related('fk_estudiante')

    # Niveles del módulo de esta clase
    niveles = Niveles.objects.filter(fk_modulo=clase.fk_modulo).order_by('orden')
    
    form = CrearEstudianteForm(initial={'clase_id': clase.cla_id})

    return render(request, 'masterdocente/clase/Matriculados_Asignados.html', {
        'clase': clase,
        'matriculas': matriculas,
        'niveles': niveles,
        'form': form,
        
    })
    
@rol_required('docente') 
def vista_tabla_matriculados_docente(request, cla_id):
    matriculas = Matriculas.objects.filter(fk_clase=cla_id).order_by(
        'fk_estudiante__fk_id_persona__fk_id_usuario__last_name',
        'fk_estudiante__fk_id_persona__per_segundo_apellido'
    )
    return render(request, 'masterdocente/clase/Tabla_Matriculados_Docente.html', {'matriculas': matriculas})



@rol_required('docente')
def crear_estudiante_docente(request):
    if request.method == 'POST':
        form = CrearEstudianteForm(request.POST)
        clase_id = request.POST.get('clase_id')

        if form.is_valid():
            try:
                with transaction.atomic():
                    email = form.cleaned_data['email']
                    cedula = form.cleaned_data['cedula']

                    user = User.objects.filter(email=email).first()
                    persona = Personas.objects.filter(per_cedula=cedula).first()

                    if not user:
                        # Crear nuevo usuario si no existe
                        user = User.objects.create(
                            username=cedula,
                            email=email,
                            first_name=form.cleaned_data['nombre'].title(),
                            last_name=form.cleaned_data['apellido'].title(),
                            password=make_password(cedula)
                        )
                        grupo_estudiantes, _ = Group.objects.get_or_create(name="Estudiantes")
                        user.groups.add(grupo_estudiantes)

                    if not persona:
                        # Crear nueva persona si no existe
                        persona = Personas.objects.create(
                            fk_id_usuario=user,
                            per_segundo_nombre=form.cleaned_data['segundo_nombre'].title(),
                            per_segundo_apellido=form.cleaned_data['segundo_apellido'].title(),
                            per_fecha_nacimiento=form.cleaned_data.get('fecha_nacimiento'),
                            per_cedula=cedula,
                            per_telefono=form.cleaned_data.get('telefono')
                        )

                    # Verificar si ya existe como estudiante
                    estudiante, creado = Estudiantes.objects.get_or_create(
                        fk_id_persona=persona,
                        defaults={
                            'est_contacto_emergencia': form.cleaned_data.get('contacto_emergencia'),
                            'est_telefono_emergencia': form.cleaned_data.get('telefono_emergencia')
                        }
                    )

                    # Verificar si ya está matriculado
                    clase = get_object_or_404(Clases, pk=clase_id)
                    ya_matriculado = Matriculas.objects.filter(fk_estudiante=estudiante, fk_clase=clase).exists()
                    if not ya_matriculado:
                        Matriculas.objects.create(fk_estudiante=estudiante, fk_clase=clase)
                        messages.success(request, 'Estudiante matriculado correctamente.')
                    else:
                        messages.info(request, 'El estudiante ya estaba matriculado en esta clase.')

                    return redirect('matriculados_asignados', clase_id=clase_id)

            except Exception as e:
                messages.error(request, f'Error al procesar: {e}')

        # Si el formulario es inválido
        clase = get_object_or_404(Clases, pk=clase_id)
        matriculas = Matriculas.objects.filter(fk_clase=clase).select_related('fk_estudiante')
        niveles = Niveles.objects.filter(fk_modulo=clase.fk_modulo).order_by('orden')

        return render(request, 'masterdocente/clase/Matriculados_Asignados.html', {
            'form': form,
            'mostrar_modal': True,
            'clase': clase,
            'matriculas': matriculas,
            'niveles': niveles,
        })

    return redirect('clase_asignada')



@require_GET
@rol_required('docente')
def obtener_datos_estudiante(request, matricula_id):
    try:
        matricula = Matriculas.objects.select_related('fk_estudiante__fk_id_persona', 'fk_estudiante__fk_id_persona__fk_id_usuario').get(pk=matricula_id)
        persona = matricula.fk_estudiante.fk_id_persona
        user = persona.fk_id_usuario

        data = {
            'matricula_id': matricula.mat_id,
            'nombre': user.first_name,
            'apellido': user.last_name,
            'email': user.email,
            'segundo_nombre': persona.per_segundo_nombre,
            'segundo_apellido': persona.per_segundo_apellido,
            'cedula': persona.per_cedula,
            'telefono': persona.per_telefono,
            'fecha_nacimiento': persona.per_fecha_nacimiento.strftime('%Y-%m-%d') if persona.per_fecha_nacimiento else '',
            'contacto_emergencia': matricula.fk_estudiante.est_contacto_emergencia,
            'telefono_emergencia': matricula.fk_estudiante.est_telefono_emergencia,
        }
        return JsonResponse({'success': True, 'data': data})
    except Matriculas.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Matrícula no encontrada'})
    
@require_POST
@rol_required('docente')
def editar_estudiante_docente(request):
    form = CrearEstudianteForm(request.POST)
    matricula_id = request.POST.get('matricula_id')

    if not matricula_id:
        messages.error(request, "ID de matrícula no recibido.")
        return redirect('clase_asignada')  # Fallback en caso de error

    if form.is_valid():
        try:
            with transaction.atomic():
                matricula = get_object_or_404(Matriculas, pk=matricula_id)
                estudiante = matricula.fk_estudiante
                persona = estudiante.fk_id_persona
                user = persona.fk_id_usuario

                # Actualizar usuario
                user.first_name = form.cleaned_data['nombre']
                user.last_name = form.cleaned_data['apellido']
                user.email = form.cleaned_data['email']
                nueva_contraseña = form.cleaned_data.get('password')
                if nueva_contraseña:
                    user.set_password(nueva_contraseña)
                user.save()

                # Actualizar persona
                persona.per_segundo_nombre = form.cleaned_data['segundo_nombre']
                persona.per_segundo_apellido = form.cleaned_data['segundo_apellido']
                persona.per_cedula = form.cleaned_data['cedula']
                persona.per_fecha_nacimiento = form.cleaned_data.get('fecha_nacimiento')
                persona.per_telefono = form.cleaned_data.get('telefono')
                persona.save()

                # Actualizar estudiante
                estudiante.est_contacto_emergencia = form.cleaned_data.get('contacto_emergencia')
                estudiante.est_telefono_emergencia = form.cleaned_data.get('telefono_emergencia')
                estudiante.save()

                messages.success(request, "Estudiante actualizado correctamente.")
        except Exception as e:
            messages.error(request, f"Error al actualizar estudiante: {str(e)}")
    else:
        messages.error(request, "Formulario inválido.")

    clase_id = form.cleaned_data.get('clase_id')
    return redirect('matriculados_asignados', clase_id=clase_id)

@require_POST
@rol_required('docente')
def eliminar_matricula(request):
    matricula_id = request.POST.get('matricula_id')
    clase_id = request.POST.get('clase_id')

    try:
        matricula = Matriculas.objects.get(pk=matricula_id)
        matricula.delete()
        messages.success(request, 'Estudiante eliminado correctamente de la clase.')
    except Matriculas.DoesNotExist:
        messages.error(request, 'No se pudo eliminar: matrícula no encontrada.')

    return redirect('matriculados_asignados', clase_id=clase_id)


#para que el docente pueda crear  masivamente matriculas
@csrf_exempt
@rol_required('docente')
def importar_estudiantes_excel_docente(request):
    if request.method == 'POST' and request.FILES.get('archivo'):
        archivo_excel = request.FILES['archivo']
        cla_id = request.POST.get('cla_id')
        clase = get_object_or_404(Clases, pk=cla_id)

        df = pd.read_excel(archivo_excel, dtype=str)

        duplicados = []
        agregados = 0
        matriculados_existentes = 0

        for index, row in df.iterrows():
            nombre = str(row.get('nombre', '')).strip().title()
            apellido = str(row.get('apellido', '')).strip().title()
            segundo_nombre = str(row.get('segundo_nombre', '')).strip().title()
            segundo_apellido = str(row.get('segundo_apellido', '')).strip().title()
            cedula = str(row.get('cedula', '')).strip().replace('.', '').replace(',', '')
            telefono = str(row.get('telefono', '')).strip().replace('.', '').replace(',', '')
            email = str(row.get('email', f"{cedula}@example.com")).strip()

            # Validación básica de cédula
            if len(cedula) < 5 or not cedula.isdigit():
                duplicados.append(f"Fila {index + 2} - Cédula inválida: {cedula}")
                continue

            # Si ya existe la persona
            persona = Personas.objects.filter(per_cedula=cedula).first()
            if persona:
                estudiante = Estudiantes.objects.filter(fk_id_persona=persona).first()
                if estudiante:
                    if Matriculas.objects.filter(fk_clase=clase, fk_estudiante=estudiante).exists():
                        duplicados.append(f"Fila {index + 2} - Estudiante ya matriculado.")
                        continue
                    Matriculas.objects.create(fk_clase=clase, fk_estudiante=estudiante)
                    matriculados_existentes += 1
                    continue

            # Crear usuario
            usuario = User.objects.create_user(
                username=cedula,
                first_name=nombre,
                last_name=apellido,
                email=email,
                password=cedula
            )

            # Asignar al grupo "Estudiantes"
            grupo_estudiantes, _ = Group.objects.get_or_create(name="Estudiantes")
            usuario.groups.add(grupo_estudiantes)

            # Crear persona sin fecha de nacimiento
            persona = Personas.objects.create(
                fk_id_usuario=usuario,
                per_segundo_nombre=segundo_nombre,
                per_segundo_apellido=segundo_apellido,
                per_cedula=cedula,
                per_telefono=telefono,
                per_fecha_nacimiento=None
            )

            # Crear estudiante
            estudiante = Estudiantes.objects.create(fk_id_persona=persona)

            # Matricular
            Matriculas.objects.create(fk_clase=clase, fk_estudiante=estudiante)
            agregados += 1

        mensaje = f"{agregados} estudiante(s) importado(s).\n{matriculados_existentes} estudiante(s) existentes fueron matriculados."

        if duplicados:
            mensaje += f"\n{len(duplicados)} advertencia(s):\n" + "\n".join(duplicados)

        return JsonResponse({'success': True, 'message': mensaje})

    return JsonResponse({'success': False, 'message': 'Solicitud inválida'})


@rol_required('docente')
def ver_notas_estudiantes(request, cla_id):
    persona = get_object_or_404(Personas, fk_id_usuario=request.user)
    docente = get_object_or_404(Docentes, fk_id_persona=persona)

    # Validar que la clase pertenece a este docente
    clase = get_object_or_404(Clases, pk=cla_id, fk_docente=docente)

    niveles = Niveles.objects.filter(fk_modulo=clase.fk_modulo).order_by('orden')
    matriculas = Matriculas.objects.filter(fk_clase=clase).order_by(
        'fk_estudiante__fk_id_persona__fk_id_usuario__last_name',
        'fk_estudiante__fk_id_persona__per_segundo_apellido'
    )

    data = []
    for matricula in matriculas:
        fila = {
            'estudiante': matricula.fk_estudiante,
            'matricula_id': matricula.mat_id, 
            'niveles': []
        }
        for nivel in niveles:
            avance = Avance_Matriculados.objects.filter(
                fk_matricula=matricula,
                fk_nivel=nivel
            ).first()

            if avance:
                fila['niveles'].append({
                    'nivel_id': nivel.niv_id,   
                    'nivel': nivel.niv_nombre,
                    'nota': avance.avm_nota_final,
                    'estado': '✅' if avance.avm_estado else '❌'
                })
            else:
                fila['niveles'].append({
                    'nivel_id': nivel.niv_id, 
                    'nivel': nivel.niv_nombre,
                    'nota': 'Sin jugar',
                    'estado': '—',
                    'nivel_estado': nivel.niv_estado
                })
        data.append(fila)

    return render(request, 'masterdocente/avance/Index.html', {
        'clase': clase,
        'niveles': niveles,
        'avance_data': data
    })