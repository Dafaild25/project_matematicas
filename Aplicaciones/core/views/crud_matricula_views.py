import pandas as pd
import openpyxl
import io
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from ..models import Matriculas, Estudiantes, Clases,Personas, Matriculas,User
from ..forms.matricula_form import MatriculasForm
from django.db import transaction
from django.http import HttpResponse
from io import BytesIO
from openpyxl import Workbook, load_workbook
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from openpyxl.utils import get_column_letter
from openpyxl.styles import Font
from django.db.models import Count



# def index(request):
#     matriculas = Matriculas.objects.all()
#     form = MatriculasForm()

#     if request.method == 'POST':
#         if 'crear_matricula' in request.POST:
#             form = MatriculasForm(request.POST)
#             if form.is_valid():
#                 form.save()
#                 messages.success(request, 'Matrícula creada correctamente.')
#                 return redirect('matricula_index')
#         elif 'editar_matricula' in request.POST:
#             mat_id = request.POST.get('mat_id')
#             matricula = get_object_or_404(Matriculas, pk=mat_id)

#             # Editar manualmente los campos
#             matricula.fk_clase_id = request.POST.get('fk_clase')
#             matricula.fk_estudiante_id = request.POST.get('fk_estudiante')
#             matricula.mat_estado = 'mat_estado' in request.POST
#             matricula.save()

#             messages.success(request, 'Matrícula actualizada correctamente.')
#             return redirect('matricula_index')

#         elif 'eliminar_matricula' in request.POST:
#             mat_id = request.POST.get('mat_id')
#             matricula = get_object_or_404(Matriculas, pk=mat_id)
#             matricula.delete()
#             messages.success(request, 'Matrícula eliminada correctamente.')
#         return redirect('matricula_index')

#     estudiantes = Estudiantes.objects.all()
#     clases = Clases.objects.filter(cla_estado=True)

#     return render(request, 'matricula/Index.html', {
#         'matriculas': matriculas,
#         'form': form,
#         'estudiantes': estudiantes,
#         'clases': clases,
#     })
    
def index(request):
    clases = Clases.objects.annotate(
        num_matriculados=Count('matriculas'),
        
    )

    return render(request, 'matricula/IndexM.html', {'clases': clases})

def detalle(request, cla_id):
    clase = get_object_or_404(Clases, pk=cla_id)
    matriculas = Matriculas.objects.filter(fk_clase=cla_id)
    estudiantes = Estudiantes.objects.all()
    return render(request, 'matricula/Detalle.html', {'matriculas': matriculas,'clase':clase, 'estudiantes': estudiantes})


def matriculaIndividual(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        cla_id = request.POST.get('cla_id')
        est_id = request.POST.get('estudiante')

        clase = get_object_or_404(Clases, pk=cla_id)
        estudiante = get_object_or_404(Estudiantes, pk=est_id)

        if Matriculas.objects.filter(fk_clase=clase, fk_estudiante=estudiante).exists():
            return JsonResponse({'success': False, 'message': 'Estudiante ya está matriculado'})

        Matriculas.objects.create(fk_clase=clase, fk_estudiante=estudiante)

        return JsonResponse({'success': True, 'message': 'Estudiante matriculado exitosamente'})

    return JsonResponse({'success': False, 'message': 'Solicitud inválida'})
    

def vista_tabla_matriculados(request, cla_id):
    matriculas = Matriculas.objects.filter(fk_clase=cla_id).order_by(
        'fk_estudiante__fk_id_persona__fk_id_usuario__last_name',
        'fk_estudiante__fk_id_persona__per_segundo_apellido'
    )
    return render(request, 'matricula/Tabla_Matriculados.html', {'matriculas': matriculas})


@require_POST
def eliminar_matricula(request, matricula_id):
    try:
        matricula = Matriculas.objects.get(pk=matricula_id)
        matricula.delete()
        return JsonResponse({'success': True, 'message': 'Matrícula eliminada correctamente'})
    except Matriculas.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Matrícula no encontrada'})


@csrf_exempt
def importar_estudiantes_excel(request):
    if request.method == 'POST' and request.FILES.get('archivo'):
        archivo_excel = request.FILES['archivo']
        cla_id = request.POST.get('cla_id')
        clase = get_object_or_404(Clases, pk=cla_id)

        df = pd.read_excel(archivo_excel, dtype=str)

        duplicados = []
        agregados = 0

        for index, row in df.iterrows():
            nombre = str(row.get('nombre', '')).strip().upper()
            apellido = str(row.get('apellido', '')).strip().upper()
            segundo_nombre = str(row.get('segundo_nombre', '')).strip().upper()
            segundo_apellido = str(row.get('segundo_apellido', '')).strip().upper()
            cedula = str(row.get('cedula', '')).strip().replace('.', '').replace(',', '')
            telefono = str(row.get('telefono', '')).strip().replace('.', '').replace(',', '')
            email = row.get('email', f"{cedula}@example.com").strip()

            # Validación de campos mínimos
            if len(cedula) < 5 or not cedula.isdigit():
                duplicados.append(f"Fila {index + 2} - Cédula inválida: {cedula}")
                continue

            # ❌ Si ya existe un usuario con esa cédula, marcar como duplicado
            if User.objects.filter(username=cedula).exists():
                duplicados.append(f"Fila {index + 2} - Cédula duplicada: {cedula}")
                continue

            # ✅ Crear usuario
            usuario = User.objects.create_user(
                username=cedula,
                first_name=nombre,
                last_name=apellido,
                email=email,
                password=cedula
            )

            # ✅ Crear persona
            persona = Personas.objects.create(
                fk_id_usuario=usuario,
                per_segundo_nombre=segundo_nombre,
                per_segundo_apellido=segundo_apellido,
                per_cedula=cedula,
                per_telefono=telefono
            )

            # ✅ Crear estudiante
            estudiante = Estudiantes.objects.create(
                fk_id_persona=persona
            )

            # ✅ Matricular si no está ya en la clase
            if not Matriculas.objects.filter(fk_clase=clase, fk_estudiante=estudiante).exists():
                Matriculas.objects.create(fk_clase=clase, fk_estudiante=estudiante)

            agregados += 1

        mensaje = f"{agregados} estudiante(s) importado(s) correctamente."

        if duplicados:
            mensaje += f" {len(duplicados)} fila(s) ignoradas por duplicidad o error:\n" + "\n".join(duplicados)

        return JsonResponse({'success': True, 'message': mensaje})

    return JsonResponse({'success': False, 'message': 'Solicitud inválida'})



def descargar_plantilla_estudiantes(request):
    # Crear archivo Excel
    wb = Workbook()
    ws = wb.active
    ws.title = "Estudiantes"

    # Encabezados ordenados y estilizados
    columnas = ['nombre', 'segundo_nombre', 'apellido', 'segundo_apellido', 'cedula', 'telefono', 'email']
    ws.append(columnas)

    for cell in ws[1]:
        cell.font = Font(bold=True)

    # Fila de ejemplo (valores como texto, conservando ceros)
    ejemplo = ['Juan', 'Carlos', 'Pérez', 'González', '0991234567', '0912345678', 'juan.perez@example.com']
    ws.append(ejemplo)

    # Aplicar formato texto explícito a cédula y teléfono (columnas 5 y 6: E y F)
    for row in ws.iter_rows(min_row=2, max_row=2, min_col=5, max_col=6):
        for cell in row:
            cell.number_format = '@'

    # Ajuste de anchos
    for col in ws.columns:
        max_length = 0
        column = col[0].column_letter
        for cell in col:
            if cell.value:
                max_length = max(max_length, len(str(cell.value)))
        ws.column_dimensions[column].width = max_length + 2

    # Preparar archivo para descarga
    output = io.BytesIO()
    wb.save(output)
    output.seek(0)

    response = HttpResponse(
        output,
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=plantilla_estudiantes.xlsx'
    return response
def importar(request):
    clases = Clases.objects.all()
    resultados = {}

    # Descargar plantilla
    if request.method == 'POST' and 'descargar_plantilla' in request.POST:
        wb = Workbook()
        ws = wb.active
        ws.title = 'Estudiantes'
        ws.append(['Nombres', 'Apellidos', 'Segundo Nombre', 'Segundo Apellido', 'Cédula', 'Teléfono', 'Fecha Nacimiento', 'Contacto Emergencia', 'Teléfono Emergencia'])

        # Exportar
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=plantilla_estudiantes.xlsx'
        wb.save(response)
        return response

    # Importar estudiantes
    elif request.method == 'POST' and 'importar_excel' in request.POST:
        archivo_excel = request.FILES.get('archivo_excel')
        clase_id = request.POST.get('fk_clase')

        if archivo_excel and clase_id:
            wb = load_workbook(filename=archivo_excel)
            ws = wb.active
            clase = Clases.objects.get(pk=clase_id)
            estudiantes_importados = []

            for i, row in enumerate(ws.iter_rows(min_row=2, values_only=True)):
                nombres, apellidos, segundo_nombre, segundo_apellido, cedula, telefono, fecha_nac, contacto_emer, tel_emer = row

                persona, creada = Personas.objects.get_or_create(
                    per_cedula=cedula,
                    defaults={
                        'fk_id_usuario_id': 1,  # Asignar usuario dummy o generar uno si hace falta
                        'per_segundo_nombre': segundo_nombre,
                        'per_segundo_apellido': segundo_apellido,
                        'per_fecha_nacimiento': fecha_nac,
                        'per_telefono': telefono,
                    }
                )

                estudiante, creado = Estudiantes.objects.get_or_create(
                    fk_id_persona=persona,
                    defaults={
                        'est_contacto_emergencia': contacto_emer,
                        'est_telefono_emergencia': tel_emer
                    }
                )

                Matriculas.objects.get_or_create(
                    fk_estudiante=estudiante,
                    fk_clase=clase
                )

                estudiantes_importados.append(estudiante)

            resultados[clase] = estudiantes_importados
            messages.success(request, "Importación realizada correctamente.")
        else:
            messages.error(request, "Debe seleccionar una clase y subir un archivo.")

    return render(request, 'matricula/Importar.html', {
        'clases': clases,
        'resultados': resultados
    })