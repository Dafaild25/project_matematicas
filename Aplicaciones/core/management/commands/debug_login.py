# Crear directorio: Aplicaciones/core/management/
# Crear directorio: Aplicaciones/core/management/commands/
# Crear archivo: Aplicaciones/core/management/__init__.py (vacío)
# Crear archivo: Aplicaciones/core/management/commands/__init__.py (vacío)
# Crear archivo: Aplicaciones/core/management/commands/debug_login.py

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group
from django.urls import reverse, resolve
from django.test import Client
import json

class Command(BaseCommand):
    help = 'Debug login system and middleware'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("=== DEBUGGING MIDDLEWARE Y URLS ===\n"))

        # 1. VERIFICAR TODAS LAS URLS
        self.stdout.write("1. VERIFICANDO URLs DISPONIBLES:")
        urls_to_check = [
            'loguin_index',
            'iniciar_sesion', 
            'cerrar_sesion',
            'core_admin',
            'core_docente',
            'core_estudiante',
            'obtener_datos_admin'
        ]

        for url_name in urls_to_check:
            try:
                url = reverse(url_name)
                self.stdout.write(f"   ✅ {url_name}: {url}")
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"   ❌ {url_name}: ERROR - {e}"))

        # 2. VERIFICAR RESOLUCIÓN DE PATHS
        self.stdout.write("\n2. VERIFICANDO RESOLUCIÓN DE PATHS:")
        paths_to_check = [
            '/',
            '/loguin/',
            '/iniciar_sesion/',
            '/cerrar_sesion/'
        ]

        for path in paths_to_check:
            try:
                resolved = resolve(path)
                self.stdout.write(f"   ✅ {path} → {resolved.url_name}")
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"   ❌ {path} → ERROR: {e}"))

        # 3. VERIFICAR GRUPOS
        self.stdout.write("\n3. VERIFICANDO GRUPOS:")
        required_groups = ['Administradores', 'Docentes', 'Estudiantes']
        for group_name in required_groups:
            group, created = Group.objects.get_or_create(name=group_name)
            status = "Creado" if created else "Existe"
            self.stdout.write(f"   ✅ {group_name}: {status}")

        # 4. VERIFICAR USUARIOS Y SUS GRUPOS
        self.stdout.write("\n4. VERIFICANDO USUARIOS:")
        users = User.objects.all()[:5]  # Solo los primeros 5
        for user in users:
            groups = [g.name for g in user.groups.all()]
            self.stdout.write(f"   Usuario: {user.username}")
            self.stdout.write(f"     - Email: {user.email}")
            self.stdout.write(f"     - Activo: {user.is_active}")
            self.stdout.write(f"     - Superuser: {user.is_superuser}")
            self.stdout.write(f"     - Grupos: {groups}")
            self.stdout.write("")

        # 5. CREAR USUARIO DE PRUEBA SI NO EXISTE
        self.stdout.write("5. CREANDO USUARIO DE PRUEBA:")
        username_test = "debug_user"
        if not User.objects.filter(username=username_test).exists():
            user = User.objects.create_user(
                username=username_test,
                email="debug@test.com",
                password="debug123",
                is_active=True
            )
            # Asignar al grupo Estudiantes
            try:
                grupo_estudiantes = Group.objects.get(name='Estudiantes')
                user.groups.add(grupo_estudiantes)
                self.stdout.write(self.style.SUCCESS(f"   ✅ Usuario '{username_test}' creado y asignado a Estudiantes"))
            except Group.DoesNotExist:
                self.stdout.write(self.style.WARNING(f"   ⚠️  Grupo 'Estudiantes' no existe"))
        else:
            self.stdout.write(f"   ℹ️  Usuario '{username_test}' ya existe")

        # 6. SIMULAR REQUESTS
        self.stdout.write("\n6. SIMULANDO REQUESTS:")
        client = Client()

        # Test 1: Acceso sin autenticación
        self.stdout.write("\n   Test 1: Acceso sin autenticación")
        try:
            response = client.get('/')
            self.stdout.write(f"     GET / → Status: {response.status_code}")
            if hasattr(response, 'url'):
                self.stdout.write(f"     Redirección: {response.url}")
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"     Error: {e}"))

        # Test 2: Acceso a login
        self.stdout.write("\n   Test 2: Acceso a login")
        try:
            response = client.get('/loguin/')
            self.stdout.write(f"     GET /loguin/ → Status: {response.status_code}")
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"     Error: {e}"))

        # 7. VERIFICAR CONFIGURACIÓN
        self.stdout.write("\n7. VERIFICANDO CONFIGURACIÓN:")
        from django.conf import settings

        self.stdout.write(f"   DEBUG: {settings.DEBUG}")
        self.stdout.write(f"   MIDDLEWARE:")
        for middleware in settings.MIDDLEWARE:
            self.stdout.write(f"     - {middleware}")

        self.stdout.write(f"\n   LOGIN_URL: {getattr(settings, 'LOGIN_URL', 'No configurado')}")
        self.stdout.write(f"   LOGOUT_REDIRECT_URL: {getattr(settings, 'LOGOUT_REDIRECT_URL', 'No configurado')}")

        self.stdout.write(self.style.SUCCESS("\n=== DEBUGGING COMPLETADO ==="))
        self.stdout.write("\nSi encuentras errores:")
        self.stdout.write("1. Revisa que las URLs estén bien definidas")
        self.stdout.write("2. Verifica que los grupos existan")
        self.stdout.write("3. Asegúrate de que los usuarios tengan grupos asignados")
        self.stdout.write("4. Revisa los logs en login_debug.log")