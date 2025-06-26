from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group
from Aplicaciones.core.models import Personas, Administradores

class Command(BaseCommand):
    help = 'Crea un usuario, persona y administrador de prueba si no existen'

    def handle(self, *args, **kwargs):
        username = 'admin1'

        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.WARNING(f"⚠️ El usuario '{username}' ya existe. No se creó nada."))
            return

        # Crear usuario
        user = User.objects.create_user(
            username=username,
            password='admin1234',
            first_name='Edison',
            last_name='Aimacaña',
            email='admin@admin.com'
        )

        # Agregar al grupo "Administradores" (créalo manualmente si no existe)
        group_name = 'Administradores'
        group, created = Group.objects.get_or_create(name=group_name)
        user.groups.add(group)

        # Crear persona
        persona = Personas.objects.create(
            fk_id_usuario=user,
            per_segundo_nombre="David",
            per_segundo_apellido="Yugsi",
            per_fecha_nacimiento="1998-06-22",
            per_cedula="1234567890",
            per_telefono="0999999999"
        )

        # Crear administrador
        Administradores.objects.create(
            fk_id_persona=persona,
            adm_estado=True
        )

        self.stdout.write(self.style.SUCCESS("✅ Usuario, Persona y Administrador creados correctamente."))