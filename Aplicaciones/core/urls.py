from django.urls import path
# views del core
from .views import core_views
from .views import crud_administrador_views
from .views import loguin_views 
from .views import crud_modulos_views
from .views import crud_niveles_views
from .views import crud_enunciado_views
from .views import crud_clase_views
from .views import crud_docente_views
from .views import crud_estudiante_views
from .views import crud_matricula_views
from .views import crud_avance_views
# VISTA DOCENTE
from .views.master_docente import docente_views
# VISTA ESTUDIANTE
from .views.master_estudiante import estudiante_views


urlpatterns = [
    
    path('', core_views.inicio, name='inicio'),
    
    #######################################CRUD ADMINISTRADOR################################
    # Vista Inicial del Administrador
    path('administrador/', crud_administrador_views.index, name='administrador_index'),
    # Vista para Crear un Administrador
    path('administrador/create', crud_administrador_views.create_administrador, name='administrador_create'),
    # Metodo para Crear un Nuevo Administrador
    path('administrador/nuevo/', crud_administrador_views.nuevo_administrador, name='administrador_nuevo'),
    # Vista para Editar un Administrador
    path('administrador/editar/<int:id_admin>/', crud_administrador_views.edit_administrador, name='administrador_edit'),
    # Metodo para Actualizar un Administrador
    path('administrador/actualizar/', crud_administrador_views.actualizar_administrador, name='administrador_actualizar'),
    # Metodo para Eliminar un Administrador
    path('administrador/eliminar/<int:id_admin>/', crud_administrador_views.eliminar_administardor, name='administrador_eliminar'),
    
    #######################################CRUD DOCENTE####################################
    # Vista Inicial del Docente
    path('docente/', crud_docente_views.index, name='docente_index'),
    # Vista para Crear un Docente
    path('docente/create', crud_docente_views.create_docente, name='docente_create'),
    # Metodo para Crear un Nuevo Docente
    path('docente/nuevo/', crud_docente_views.nuevo_docente, name='docente_nuevo'),
    # Vista para Editar un Docente
    path('docente/editar/<int:id_docen>/',crud_docente_views.edit_docente, name='docente_edit'),
    # Metodo para Actualizar un Docente
    path('docente/actualizar/', crud_docente_views.actualizar_docente, name='docente_actualizar'),
    # Metodo para Eliminar un Docente
    path('docente/eliminar/<int:id_docen>/', crud_docente_views.eliminar_docente, name='docente_eliminar'),
    
    #######################################CRUD ESTUDIANTE###################################
    # Vista Inicial del Estudiante
    path('estudiante/', crud_estudiante_views.index, name='estudiante_index'),
    # Vista para Crear un Estudiante
    path('estudiante/create', crud_estudiante_views.create_estudiante, name='estudiante_create'),
    # Metodo para Crear un Nuevo Estudiante
    path('estudiante/nuevo/', crud_estudiante_views.nuevo_estudiante, name='estudiante_nuevo'),
    # Vista para Editar un Estudiante
    path('estudiante/editar/<int:id_estud>/',crud_estudiante_views.edit_estudiante, name='estudiante_edit'),
    # Metodo para Actualizar un Estudiante
    path('estudiante/actualizar/', crud_estudiante_views.actualizar_estudiante, name='estudiante_actualizar'),
    # Metodo para Eliminar un Estudiante
    path('estudiante/eliminar/<int:id_estud>/', crud_estudiante_views.eliminar_estudiante, name='estudiante_eliminar'),

    ########################################VISTA DOCENTE###################################
    # Vista Inicial del Docente
    path('docente/vista/', docente_views.vista_docente, name='docente_vista'),

    ########################################VISTA ESTUDIANTE##################################
    # Vista Inicial del Estudiante
    path('estudiante/vista/', estudiante_views.vista_estudiante, name='estudiante_vista'),


    # Ruta para generar un  crud completo en un mismo template con modal
    path('modulo/', crud_modulos_views.index, name='modulo_index'),
    
    #Ruta para genera un crud completo de los niveles
    path('nivel/', crud_niveles_views.index, name='nivel_index'),
    
    #Ruta para listar enunciados
    path('enunciado/', crud_enunciado_views.index, name='enunciado_index'),
    path('ajax/niveles/', crud_enunciado_views.cargar_niveles, name='ajax_cargar_niveles'),
    path('enunciado/create', crud_enunciado_views.create, name='enunciado_create'),
    path('enunciado/editar/<int:enun_id>', crud_enunciado_views.editar, name='enunciado_editar'),
    path('enunciado/eliminar/<int:enun_id>', crud_enunciado_views.eliminar, name='enunciado_eliminar'),
    
    
    
    
    
    #Ruta para generar un crud de clases
    path('clase/', crud_clase_views.index, name='clase_index'),
    
    
    # Ruta para crear las matriculas
    #path('matricula/', crud_matricula_views.index, name='matricula_index'),
    path('matricula/', crud_matricula_views.index, name='matricula_index'),
    path('matricula/detalle/<int:cla_id>', crud_matricula_views.detalle, name='matricula_detalle'),
    path('matricula/individual/', crud_matricula_views.matriculaIndividual, name='matricula_individual'),
    path('matricula/listado/<int:cla_id>/',crud_matricula_views.vista_tabla_matriculados, name='matricula_listado'),
    path('matriculas/eliminar/<int:matricula_id>/', crud_matricula_views.eliminar_matricula, name='eliminar_matricula'),
    path('matricula/importar', crud_matricula_views.importar_estudiantes_excel, name='importar_matricula_excel'),
    path('matricula/descargar-plantilla/',crud_matricula_views.descargar_plantilla_estudiantes, name='descargar_plantilla_estudiantes'),
    
    #Ruta para ver los avnces de los estudiantes en modo administrador
    path('avance/<int:cla_id>/', crud_avance_views.index, name='avance_index'),

    
    
    #path('matricula/importar', crud_matricula_views.importar, name='matricula_importar'),

    ########################################LOGUIN########################################
    # Vista de Formulario de Inicio de Sesión
    path('loguin/', loguin_views.index, name='loguin_index'),
    # Metodo para Iniciar Sesión
    path('iniciar_sesion/', loguin_views.iniciar_sesion, name='iniciar_sesion'),

    ########################################LOGOUT#######################################
    # Metodo para Cerrar Sesión
    path('cerrar_sesion/',loguin_views.cerrar_sesion, name='cerrar_sesion'),
    

]