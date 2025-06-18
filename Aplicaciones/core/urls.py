from django.urls import path

# views del core
from .views import core_views
from .views import crud_administrador_views
from .views import crud_docente_views
from .views import crud_estudiante_views


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

]