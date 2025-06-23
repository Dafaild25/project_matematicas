from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group
from Aplicaciones.core.models import Personas, Estudiantes  # Asegúrate que esté correctamente importado

class Command(BaseCommand):
    help = 'Crea un usuario, persona y estudiante de prueba si no existen'

    def handle(self, *args, **kwargs):
        username = 'estudiante1'

        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.WARNING(f"⚠️ El usuario '{username}' ya existe. No se creó nada."))
            return

        # Crear el usuario
        user = User.objects.create_user(
            username=username,
            password='estudiante1234',
            first_name='Luis',
            last_name='Salazar',
            email='estudiante1@correo.com'
        )

        # Agregar al grupo "Estudiantes"
        grupo, _ = Group.objects.get_or_create(name='Estudiantes')
        user.groups.add(grupo)

        # Crear la persona
        persona = Personas.objects.create(
            fk_id_usuario=user,
            per_segundo_nombre="Enrique",
            per_segundo_apellido="Mora",
            per_fecha_nacimiento="2005-09-10",
            per_cedula="0987654321",
            per_telefono="0981234567"
        )

        # Crear el estudiante
        Estudiantes.objects.create(
            fk_id_persona=persona,
            est_estado=True  # Ajusta según tu modelo
        )

        self.stdout.write(self.style.SUCCESS("✅ Usuario, Persona y Estudiante creados correctamente."))
