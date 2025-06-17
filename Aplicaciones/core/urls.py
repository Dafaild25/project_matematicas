from django.urls import path

# views del core
from .views import core_views
from .views import crud_administrador_views
from .views import loguin_views 
from .views import crud_modulos_views
from .views import crud_niveles_views
from .views import crud_enunciado_views


urlpatterns = [
    
    path('', core_views.inicio, name='inicio'),
    
    #######################################CRUD ADMINISTRADOR#######################################
    # Vista Inicial del Administrador
    path('administrador/', crud_administrador_views.index, name='administrador_index'),
    # Vista para Crear un Administrador
    path('administrador/create', crud_administrador_views.create, name='administrador_create'),
    # Metodo para Crear un Nuevo Administrador
    path('administrador/nuevo/', crud_administrador_views.nuevo_administrador, name='administrador_nuevo'),
    # Vista para Editar un Administrador
    path('administrador/editar/<int:id_admin>/', crud_administrador_views.edit, name='administrador_edit'),
    # Metodo para Actualizar un Administrador
    path('administrador/actualizar/', crud_administrador_views.actualizar_administrador, name='administrador_actualizar'),
    
    
    
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

    
    
    
    
    
    
    
    
    
    
    # loguin
    path('loguin/', loguin_views.index, name='loguin_index'),
    
]