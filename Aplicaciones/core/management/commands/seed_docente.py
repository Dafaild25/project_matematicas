from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group
from Aplicaciones.core.models import Personas, Docentes  # Asegúrate de tener el modelo Docentes

class Command(BaseCommand):
    help = 'Crea un usuario, persona y docente de prueba si no existen'

    def handle(self, *args, **kwargs):
        username = 'docente1'

        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.WARNING(f"⚠️ El usuario '{username}' ya existe. No se creó nada."))
            return

        # Crear usuario
        user = User.objects.create_user(
            username=username,
            password='docente1234',
            first_name='María',
            last_name='Quishpe',
            email='docente1@correo.com'
        )

        # Agregar al grupo "Docentes"
        group_name = 'Docentes'
        group, _ = Group.objects.get_or_create(name=group_name)
        user.groups.add(group)

        # Crear persona
        persona = Personas.objects.create(
            fk_id_usuario=user,
            per_segundo_nombre="Isabel",
            per_segundo_apellido="Cando",
            per_fecha_nacimiento="1985-03-10",
            per_cedula="1122334455",
            per_telefono="0987654321"
        )

        # Crear docente (ajusta los campos según tu modelo)
        Docentes.objects.create(
            fk_id_persona=persona,
            doc_estado=True  # o los campos que tenga tu modelo
        )

        self.stdout.write(self.style.SUCCESS("✅ Usuario, Persona y Docente creados correctamente."))
