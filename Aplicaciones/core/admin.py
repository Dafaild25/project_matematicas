from django.contrib import admin
from .models import * # Importar modelos

# Register your models here.
admin.site.register(Personas)
admin.site.register(Administradores)
admin.site.register(Docentes)
admin.site.register(Estudiantes)
