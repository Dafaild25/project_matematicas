from django.core.management.base import BaseCommand
from Aplicaciones.core.models import Modulos, Niveles
from django.utils.timezone import now

class Command(BaseCommand):
    help = 'Crea 3 módulos con 3 niveles cada uno (Fácil, Medio, Difícil)'

    def handle(self, *args, **kwargs):
        # Borrar datos anteriores
        Niveles.objects.all().delete()
        Modulos.objects.all().delete()

        modulos = []
        for i in range(1, 4):
            modulo = Modulos.objects.create(
                mod_nombre=f"Módulo {i}",
                mod_descripcion=f"Descripción del módulo {i}",
                mod_estado=True,
                mod_fecha_creacion=now(),
                mod_fecha_actualizacion=now()
            )
            modulos.append(modulo)

        descripciones = ["Fácil", "Medio", "Difícil"]
        for modulo in modulos:
            for orden, desc in enumerate(descripciones, start=1):
                Niveles.objects.create(
                    fk_modulo=modulo,
                    niv_nombre=f"Nivel {orden} - {desc}",
                    niv_descripcion=desc,
                    orden=orden,
                    vidas=5,
                    ruta="Sin ruta",
                    niv_estado=True,
                    niv_fecha_creacion=now(),
                    niv_fecha_actualizacion=now()
                )

        self.stdout.write(self.style.SUCCESS("✅ Seeding completado: 3 módulos y 9 niveles (Fácil, Medio, Difícil) creados."))
