from django.urls import path

# views del core
from .views import core_views
from .views import crud_administrador_views


urlpatterns = [
    
    path('', core_views.inicio, name='inicio'),
    
    # Crud administrador
    path('administrador/', crud_administrador_views.index, name='administrador_index'),
    path('administrador/crear/', crud_administrador_views.create, name='administrador_create'),
    
]