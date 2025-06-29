from django.urls import path
from django.contrib.auth.views import PasswordChangeView # Importar vista de cambio de contraseña propia de Django

# views del core
from .views import core_views
from .views import crud_administrador_views

from .views.cuestionario_Modulo1 import  get_game_info, save_attempt, update_best_score, check_lives_status
from .views.master_docente.demos_docente import  docente_ver_niveles_modulo, docente_probar_nivel


from .views import loguin_views 
from .views import crud_modulos_views
from .views import crud_niveles_views

from .views import crud_clase_views
from .views import crud_docente_views
from .views import crud_estudiante_views
from .views import crud_matricula_views
from .views import crud_avance_views
# VISTA DOCENTE
from .views.master_docente import docente_perfil_views
from .views.master_docente import core_docente_views
from .views.master_docente import clases_asignadas_docente_views
from .views.master_docente import avance_matriculados_docente_views
# VISTA REPORTES DOCENTE
from .views.master_docente import reportes_docente
# VISTA ESTUDIANTE
from .views.master_estudiante import estudiante_perfil_views
from .views.master_estudiante import core_estudiante_views
from .views.master_estudiante import estudiante_modulo_views
#REPORTE-HISTORIAL
from .views.reportehistorial import historial_intentos_views
#REPORTE ADMIN
from .views.reportehistorial import reportes_docente_para_admin_views



urlpatterns = [
    
    # ===== URLS DE AUTENTICACIÓN =====
    # Página de inicio/login - esta debe ser la raíz
    path('', loguin_views.index, name='loguin_index'),
    path('loguin/', loguin_views.index, name='loguin_index_alt'),  # URL alternativa
    
    # Métodos de autenticación
    path('iniciar_sesion/', loguin_views.iniciar_sesion, name='iniciar_sesion'),
    path('cerrar_sesion/', loguin_views.cerrar_sesion, name='cerrar_sesion'),
    
    
    # urrl del core  administrador
    path('core/admin/', core_views.dashboard_admin, name='core_admin'),
    path('admin/dashboard/data/', core_views.obtener_datos_admin, name='obtener_datos_admin'),

    ########################################CAMBIO DE CONTRASEÑA################################ no  toque
    # Vista para Cambiar la Contraseña del Usuario
    path('cambiar_contrasena/', PasswordChangeView.as_view(template_name='usuarios/cambiar_contrasena.html'), name='cambiar_contrasena'),
    
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
    # Metodo para Descargar Plantilla de Docente
    path('docente/plantilla/', crud_docente_views.descargar_plantilla_docentes, name='descargar_plantilla_docentes'),
    # Metodo para Importar Docentes Masivamente
    path('docente/importar/', crud_docente_views.importar_docentes_excel, name='importar_docentes_excel'),
    # Metodo para Exportar Docentes
    path('docente/exportar/', crud_docente_views.exportar_docentes, name='exportar_docentes'),
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




    
    #######################################CRUD MODULO###################################
    path('modulo/', crud_modulos_views.index, name='modulo_index'),
    
    #######################################CRUD NIVEL###################################
    path('nivel/', crud_niveles_views.index, name='nivel_index'),
    
   
    
    
    
    
    
    #######################################CRUD CLASES###################################
    path('clase/', crud_clase_views.index, name='clase_index'),
    
    
    #######################################CRUD MATRULICULAS###################################
    #path('matricula/', crud_matricula_views.index, name='matricula_index'),
    path('matricula/', crud_matricula_views.index, name='matricula_index'),
    path('matricula/detalle/<int:cla_id>', crud_matricula_views.detalle, name='matricula_detalle'),
    path('matricula/individual/', crud_matricula_views.matriculaIndividual, name='matricula_individual'),
    path('matricula/listado/<int:cla_id>/',crud_matricula_views.vista_tabla_matriculados, name='matricula_listado'),
    path('matriculas/eliminar/<int:matricula_id>/', crud_matricula_views.eliminar_matricula, name='eliminar_matricula'),
    path('matricula/importar', crud_matricula_views.importar_estudiantes_excel, name='importar_matricula_excel'),
    path('matricula/descargar-plantilla/',crud_matricula_views.descargar_plantilla_estudiantes, name='descargar_plantilla_estudiantes'),  #Usado por admin y docente
    
    #######################################CONSULTA DE AVANCE###################################
    path('avance/<int:cla_id>/', crud_avance_views.index, name='avance_index'),

    
    
    ########################################VISTA DOCENTE###################################
    # Vista Inicial del Docente
    path('core/docente/', core_docente_views.dashboard_docente, name='core_docente'),
    # Vista Editar Perfil del Docente
    path('docente/perfil/', docente_perfil_views.editar_perfil_docente, name='editar_perfil_docente'),
    # Metodo para Actualizar el Perfil del Docente
    path('docente/perfil/actualizar/', docente_perfil_views.actualizar_perfil_docente, name='actualizar_perfil_docente'),
    path('dashboard/obtener_datos/', core_docente_views.obtener_datos_dashboard, name='obtener_datos_dashboard'),
    path('docente/clase/', clases_asignadas_docente_views.clases_asignadas_docente, name='clase_asignada'),
    path('docente/matriculados/<int:clase_id>/', clases_asignadas_docente_views.matriculados_asignados_docente, name='matriculados_asignados'),
    path('docente/clase/<int:cla_id>/tabla-matriculados/', clases_asignadas_docente_views.vista_tabla_matriculados_docente, name='tabla_matriculados_docente'),
    path('docente/crear-estudiante/', clases_asignadas_docente_views.crear_estudiante_docente, name='crear_estudiante_docente'),
    path('ajax/estudiante/<int:matricula_id>/', clases_asignadas_docente_views.obtener_datos_estudiante, name='ajax_datos_estudiante'),
    path('editar-estudiante/', clases_asignadas_docente_views.editar_estudiante_docente, name='editar_estudiante_docente'),
    path('eliminar-matricula/', clases_asignadas_docente_views.eliminar_matricula, name='eliminar_matricula'),
    path('docente/importar-estudiantes/', clases_asignadas_docente_views.importar_estudiantes_excel_docente, name='importar_estudiantes_excel_docente'),
    #vista para ver el avance los  estudiantes a su cargo 
    path('docente/clase/<int:cla_id>/notas/', clases_asignadas_docente_views.ver_notas_estudiantes, name='ver_notas_estudiantes'),
    path('historial-intentos/', avance_matriculados_docente_views.historial_intentos, name='historial_intentos'),
    path('asignar-vidas/', avance_matriculados_docente_views.asignar_vidas, name='asignar_vidas_docente'),

    #VISTA DE REPORTES DE AVANCES DE LOS ESTUDIANTES PARA EL DOCENTE
    path('pdf/nivel/<int:clase_id>/<int:nivel_id>/', reportes_docente.generar_pdf_nivel, name='pdf_nivel'),
    path('pdf/general/<int:clase_id>/', reportes_docente.generar_pdf_general, name='pdf_general'),
    
    #VISTA DE REPORTES DE AVANCES DE LOS ESTUDIANTES PARA EL ADMIN
    path('pdf/nivel/admin/<int:clase_id>/<int:nivel_id>/', reportes_docente_para_admin_views.generar_pdf_nivel_admin, name='pdf_nivel_admin'),
    path('pdf/general/admin/<int:clase_id>/', reportes_docente_para_admin_views.generar_pdf_general_admin, name='pdf_general_admin'),
  




    

    ########################################VISTA ESTUDIANTE##################################
    # Vista Inicial del Estudiante
    path('core/estudiante/', core_estudiante_views.core_estudiante, name='core_estudiante'),
    # Vista Editar Perfil del Estudiante
    path('estudiante/perfil/', estudiante_perfil_views.editar_perfil_estudiante, name='editar_perfil_estudiante'),
    # Metodo para Actualizar el Perfil del Estudiante
    path('estudiante/perfil/actualizar/',estudiante_perfil_views.actualizar_perfil_estudiante, name='actualizar_perfil_estudiante'),
    path('estudiante/modulo/', estudiante_modulo_views.estudiante_modulo, name='estudiante_modulo'),
    path('modulo/<int:modulo_id>/niveles/', estudiante_modulo_views.ver_niveles_modulo, name='ver_niveles_modulo'),
    
    
    ########################################Juego del Modulo  ##################################
    path('nivel/<int:nivel_id>/jugar/', estudiante_modulo_views.jugar_nivel, name='jugar_nivel'),

    # URLs para docentes
    
    path('docente/modulo/<int:modulo_id>/niveles/', docente_ver_niveles_modulo, name='docente_ver_niveles_modulo'),
    path('docente/nivel/<int:nivel_id>/probar/', docente_probar_nivel, name='docente_probar_nivel'),



    # Cuestionario Modulo 1
    #path('cuestionario_Modulo1/', cuestionario_Modulo1, name='cuestionario_Modulo1'),
    # URLs para el sistema de calificaciones
    path('get_game_info/', get_game_info, name='get_game_info'),
    path('save_attempt/', save_attempt, name='save_attempt'),
    path('update_best_score/', update_best_score, name='update_best_score'),
    path('check_lives_status/', check_lives_status, name='check_lives_status'),
    
    
    
    ######################################## REPORTE HISTORIAL DE INTENTOS ####################################
    path('reporte-intento/<int:matricula_id>/<int:nivel_id>/', historial_intentos_views.generar_reporte_intento_individual_pdf, name='reporte_intento_individual'),
    path('reporte-intento/admin/<int:matricula_id>/<int:nivel_id>/', historial_intentos_views.generar_reporte_intento_individual_admin_pdf, name='reporte_intento_individual_admin'),



]