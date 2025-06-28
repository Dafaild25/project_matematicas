from django.core.management.base import BaseCommand
from Aplicaciones.core.models import Modulos, Niveles
from django.utils.timezone import now

class Command(BaseCommand):
    help = 'Crea 3 módulos con 3 niveles cada uno (Fácil, Medio, Difícil) con rutas personalizadas'

    def handle(self, *args, **kwargs):
        # Borrar datos anteriores
        Niveles.objects.all().delete()
        Modulos.objects.all().delete()

        modulos = []
        for i in range(1, 4):  # Crear 3 módulos
            modulo = Modulos.objects.create(
                mod_nombre=f"Módulo {i}",
                mod_descripcion=f"Descripción del módulo {i}",
                mod_estado=True,
                mod_fecha_creacion=now(),
                mod_fecha_actualizacion=now()
            )
            modulos.append(modulo)

        descripciones = ["Fácil", "Medio", "Difícil"]
        nombres_ruta = ["Primer_Nivel", "Segundo_Nivel", "Tercer_Nivel"]

        for modulo in modulos:
            for orden, (desc, nombre_ruta) in enumerate(zip(descripciones, nombres_ruta), start=1):
                ruta = f"masterestudiante/juego/modulo-{modulo.mod_id}/{nombre_ruta}.html"
                Niveles.objects.create(
                    fk_modulo=modulo,
                    niv_nombre=f"Nivel {orden} - {desc}",
                    niv_descripcion=desc,
                    orden=orden,
                    vidas=5,
                    ruta=ruta,
                    niv_estado=True,
                    niv_fecha_creacion=now(),
                    niv_fecha_actualizacion=now()
                )

        self.stdout.write(self.style.SUCCESS("✅ Se crearon 3 módulos y 9 niveles con rutas correctamente configuradas."))
