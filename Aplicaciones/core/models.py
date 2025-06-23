from django.db import models
from django.contrib.auth.models import User,Group
from django.utils import timezone

# MODULO PERSONAS
class Personas(models.Model):
    per_id = models.AutoField(primary_key=True)
    # Clave foranea User
    fk_id_usuario = models.ForeignKey(User,verbose_name='Usuario',on_delete=models.CASCADE)
    per_segundo_nombre = models.CharField(max_length=50,default="Null",null=False,verbose_name="Segundo nombre:")
    per_segundo_apellido = models.CharField(max_length=50,default="Null",null=False,verbose_name="Segundo apellido:")
    per_fecha_nacimiento = models.DateField(default="Null",verbose_name="Fecha de nacimiento:")
    per_cedula = models.CharField(max_length=15,default="Null",null=False,verbose_name="Cédula:")
    per_telefono = models.CharField(max_length=15,default="Null",null=True,verbose_name="Teléfono:")
    per_fecha_actualizacion = models.DateTimeField(auto_now=True,verbose_name='Actualizado el:')
    # Mejorar presentacion de los datos
    def __str__(self):
        # Obtener grupo al que pertenece
        grupo = self.fk_id_usuario.groups.first()
        nombre_grupo = grupo.name
        nombre_grupo = grupo.name if grupo else "Sin grupo definido" # Validar que exita en un grupo

        fila = "{0}: {1} {2} - {3}" # Debo mostrar el grupo al que pertenece
        return fila.format(self.per_id,self.fk_id_usuario.first_name,self.fk_id_usuario.last_name,nombre_grupo)
    
# MODULO ADMINISTRADORES
class Administradores(models.Model):
    adm_id = models.AutoField(primary_key=True)
    # Clave foranea Persona
    fk_id_persona = models.ForeignKey(Personas,verbose_name='Persona',on_delete=models.CASCADE)
    adm_fotografia = models.ImageField(default='Sin Foto',null=True,blank=True,verbose_name="Fotografía:")
    adm_estado = models.BooleanField(default=True,verbose_name='Estado:')
    
    def __str__(self):
        return f"{self.adm_id}: {self.fk_id_persona.fk_id_usuario.first_name} {self.fk_id_persona.fk_id_usuario.last_name}"
    
# MODULO DOCENTES
class Docentes(models.Model):
    doc_id = models.AutoField(primary_key=True)
    # Clave foranea Persona
    fk_id_persona = models.ForeignKey(Personas,verbose_name='Persona',on_delete=models.CASCADE)
    doc_cargo = models.CharField(max_length=100,default="Null",null=False,verbose_name="Cargo:")
    doc_fotografia = models.ImageField(upload_to='docentes/',default='Sin Foto',verbose_name="Fotografía:")
    doc_estado = models.BooleanField(default=True,verbose_name='Estado:')
    
    def __str__(self):
        return f"{self.doc_id}: {self.fk_id_persona.fk_id_usuario.first_name} {self.fk_id_persona.fk_id_usuario.last_name}"
    
# MODULO ESTUDIANTES
class Estudiantes(models.Model):
    est_id = models.AutoField(primary_key=True)
    # Clave foranea Persona
    fk_id_persona = models.ForeignKey(Personas,verbose_name='Persona',on_delete=models.CASCADE)
    est_contacto_emergencia = models.CharField(max_length=50,default="Null",null=True,verbose_name="Contacto de emergencia:")
    est_telefono_emergencia = models.CharField(max_length=15,default="Null",null=True,verbose_name="Teléfono de emergencia:")
    est_fotografia = models.ImageField(upload_to='estudiantes/',default='Sin Foto',null=True,blank=True,verbose_name="Fotografía:")
    est_estado = models.BooleanField(default=True,verbose_name='Estado:')
    def __str__(self):
        return f"{self.est_id}: {self.fk_id_persona.fk_id_usuario.first_name} {self.fk_id_persona.fk_id_usuario.last_name}"
    
# MODULO MODULOS  (5,6,7 años) 
class Modulos(models.Model):
    mod_id = models.AutoField(primary_key=True)
    mod_nombre = models.CharField(max_length=50,null=False,unique=True,verbose_name="Nombre del modulo:")
    mod_descripcion = models.CharField(max_length=100,null=False,verbose_name="Descripción del modulo:")
    mod_estado = models.BooleanField(default=True,verbose_name='Estado:')
    mod_fecha_creacion = models.DateTimeField(auto_now_add=True,verbose_name='Creado el:')
    mod_fecha_actualizacion = models.DateTimeField(auto_now=True,verbose_name='Actualizado el:')
    
    def __str__(self):
        return f"{self.mod_id}: {self.mod_nombre}"
    
# MODULO NIVELES

class Niveles(models.Model):
    niv_id = models.AutoField(primary_key=True)
    fk_modulo = models.ForeignKey(Modulos,verbose_name='Modulo',on_delete=models.CASCADE)
    niv_nombre = models.CharField(max_length=50,null=False,unique=True,verbose_name="Nombre del nivel:")
    niv_descripcion = models.CharField(max_length=100,null=False,verbose_name="Descripción del nivel:")
    orden = models.IntegerField()
    vidas = models.IntegerField()
    niv_estado = models.BooleanField(default=True,verbose_name='Estado:')
    niv_fecha_creacion = models.DateTimeField(auto_now_add=True,verbose_name='Creado el:')
    niv_fecha_actualizacion = models.DateTimeField(auto_now=True,verbose_name='Actualizado el:')
    
    def __str__(self):
        return f"{self.niv_id}: {self.niv_nombre}"

class Enunciados(models.Model):
    enun_id = models.AutoField(primary_key=True)
    fk_nivel = models.ForeignKey(Niveles,verbose_name='Nivel',on_delete=models.CASCADE)
    enun_nombre = models.CharField(max_length=100,null=False,verbose_name="Enunciado:")
    enun_estado = models.BooleanField(default=True,verbose_name='Estado:')
    enun_fecha_creacion = models.DateTimeField(auto_now_add=True,verbose_name='Creado el:')
    enun_fecha_actualizacion = models.DateTimeField(auto_now=True,verbose_name='Actualizado el:')
    
    def __str__(self):
        return f"{self.enun_id}: {self.enun_nombre}"
    

class Preguntas(models.Model):
    pre_id = models.AutoField(primary_key=True)
    fk_enunciado = models.ForeignKey(Enunciados,verbose_name='Enunciado',on_delete=models.CASCADE)
    pre_nombre= models.CharField(max_length=100,null=False,verbose_name="Pregunta:")
    pre_tiene_imagen = models.BooleanField(default=False,verbose_name='Tiene imagen:')
    pre_imagen = models.ImageField(upload_to='preguntas/',default='Sin Foto',null=True,blank=True,verbose_name="Imagen:")
    pre_estado = models.BooleanField(default=True,verbose_name='Estado:')
    pre_fecha_creacion = models.DateTimeField(auto_now_add=True,verbose_name='Creado el:')
    pre_fecha_actualizacion = models.DateTimeField(auto_now=True,verbose_name='Actualizado el:')
    
    def __str__(self):
        return f"{self.pre_id}: {self.pre_nombre} "

class Opciones(models.Model):
    op_id = models.AutoField(primary_key=True)
    fk_pregunta = models.ForeignKey(Preguntas,verbose_name='Pregunta',on_delete=models.CASCADE)
    op_nombre = models.CharField(max_length=100,null=False,verbose_name="Opcion:")
    op_correcta = models.BooleanField(default=False,verbose_name='Correcta:')
    op_estado = models.BooleanField(default=True,verbose_name='Estado:')
    op_fecha_creacion = models.DateTimeField(auto_now_add=True,verbose_name='Creado el:')
    op_fecha_actualizacion = models.DateTimeField(auto_now=True,verbose_name='Actualizado el:')
    
    def __str__(self):
        return f"{self.op_id}: {self.op_nombre}"


class Clases (models.Model):
    cla_id = models.AutoField(primary_key=True)
    fk_docente = models.ForeignKey(Docentes,verbose_name='Docente',on_delete=models.CASCADE)
    fk_modulo = models.ForeignKey(Modulos,verbose_name='Modulo',on_delete=models.CASCADE)
    cla_nombre = models.CharField(max_length=100,null=False,verbose_name="Clase:")
    cla_estado = models.BooleanField(default=True,verbose_name='Estado:')
    cla_fecha_creacion = models.DateTimeField(auto_now_add=True,verbose_name='Creado el:')
    cla_fecha_actualizacion = models.DateTimeField(auto_now=True,verbose_name='Actualizado el:')
    
    def __str__(self):
        return f" {self.cla_nombre}"    

class Matriculas(models.Model):
    mat_id = models.AutoField(primary_key=True)
    fk_estudiante = models.ForeignKey(Estudiantes,verbose_name='Estudiante',on_delete=models.CASCADE)
    fk_clase = models.ForeignKey(Clases,verbose_name='Clase',on_delete=models.CASCADE)
    mat_estado = models.BooleanField(default=True,verbose_name='Estado:')
    mat_fecha_creacion = models.DateTimeField(auto_now_add=True,verbose_name='Creado el:')
    mat_fecha_actualizacion = models.DateTimeField(auto_now=True,verbose_name='Actualizado el:')



class IntentoNivel(models.Model):
    
    fk_matricula = models.ForeignKey(Matriculas,verbose_name='Matricula',on_delete=models.CASCADE)
    fk_nivel = models.ForeignKey(Niveles,verbose_name='Niveles',on_delete=models.CASCADE)
    in_nota = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Nota obtenida en el intento"
    )
    in_fecha_creacion = models.DateTimeField(auto_now_add=True,verbose_name='Creado el:')
    in_fecha_actualizacion = models.DateTimeField(auto_now=True,verbose_name='Actualizado el:')
    in_vidas_usadas = models.IntegerField(
        
        blank=True,
        null=True,
        help_text="Número de vidas utilizadas en el intento"
    )

    class Meta:
        db_table = 'intento_nivel'
        verbose_name = 'Intento de Nivel'
        verbose_name_plural = 'Intentos de Nivel'
        ordering = ['-in_fecha_creacion']

    def __str__(self):
        return f"Intento de {self.estudiante.username if self.estudiante else 'Usuario'} - Nivel {self.nivel.id if self.nivel else 'N/A'} - Nota: {self.nota}"




class Avance_Matriculados(models.Model):
    ESTADOS_CHOICES = [
        ('iniciado', 'Iniciado'),
        ('en_progreso', 'En Progreso'),
        ('completado', 'Completado'),
        ('aprobado', 'Aprobado'),
        ('reprobado', 'Reprobado'),
        ('sin_vidas', 'Sin Vidas'),
    ]
    
    avm_id = models.AutoField(primary_key=True)
    fk_matricula = models.ForeignKey(Matriculas, verbose_name='Matricula', on_delete=models.CASCADE)
    fk_nivel = models.ForeignKey(Niveles, verbose_name='Niveles', on_delete=models.CASCADE)
    avm_nota_final = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Mejor nota obtenida en el nivel"
    )
    # Corregido: era BooleanField con choices, ahora es CharField
    avm_estado = models.CharField(
        max_length=20,
        choices=ESTADOS_CHOICES,
        default='iniciado',
        blank=True,
        null=True
    )
    avm_fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name='Creado el:')
    avm_fecha_actualizacion = models.DateTimeField(auto_now=True, verbose_name='Actualizado el:')
    
    # NUEVO CAMPO PARA VIDAS RESTANTES
    avm_vidas_restantes = models.IntegerField(
       
        blank=True,
        null=True,
        help_text="Vidas restantes para este nivel"
    )
    
    # NUEVO CAMPO PARA RASTREAR FECHA DE ÚLTIMO INTENTO
    avm_ultimo_intento = models.DateTimeField(
        blank=True,
        null=True,
        help_text="Fecha del último intento realizado"
    )
    
    # NUEVO CAMPO PARA GUARDAR LAS VIDAS INICIALES DEL NIVEL
    avm_vidas_iniciales_nivel = models.IntegerField(
        
        blank=True,
        null=True,
        help_text="Vidas iniciales que tenía el nivel cuando el estudiante se matriculó"
    )

    class Meta:
        db_table = 'avance_estudiante'
        verbose_name = 'Avance de Estudiante'
        verbose_name_plural = 'Avances de Estudiantes'
        # Corregido: usar los nombres correctos de campos
        unique_together = ['fk_matricula', 'fk_nivel']
        ordering = ['fk_matricula', 'fk_nivel']

    def __str__(self):
        # Corregido: usar los nombres correctos de campos y relaciones
        return f"Avance de {self.fk_matricula.fk_estudiante.username if self.fk_matricula and self.fk_matricula.fk_estudiante else 'Usuario'} - Nivel {self.fk_nivel.niv_id if self.fk_nivel else 'N/A'} - Estado: {self.avm_estado}"
    
    # MÉTODO PARA INICIALIZAR VIDAS CUANDO UN ESTUDIANTE ACCEDE POR PRIMERA VEZ
    def inicializar_vidas(self):
        """Inicializa las vidas restantes basándose en el nivel"""
        if self.avm_vidas_restantes is None or self.avm_vidas_restantes == 0:
            # Asumiendo que el campo de vidas en Niveles se llama niv_vidas
            self.avm_vidas_restantes = self.fk_nivel.niv_vidas  
            self.avm_vidas_iniciales_nivel = self.fk_nivel.niv_vidas
            self.save()
    
    # MÉTODO PARA USAR UNA VIDA
    def usar_vida(self):
        """Reduce una vida y actualiza el estado si es necesario"""
        if self.avm_vidas_restantes > 0:
            self.avm_vidas_restantes -= 1
            self.avm_ultimo_intento = timezone.now()
            
            if self.avm_vidas_restantes == 0:
                self.avm_estado = 'sin_vidas'
            
            self.save()
            return True
        return False
    
    # MÉTODO PARA VERIFICAR SI PUEDE HACER UN INTENTO
    def puede_intentar(self):
        """Verifica si el estudiante puede hacer un intento"""
        return self.avm_vidas_restantes > 0 and self.avm_estado != 'sin_vidas'
    
    # MÉTODO DE INSTANCIA para verificar y restaurar vidas por cambios del admin
    def restaurar_vidas_por_cambio_admin(self):
        """
        Verifica si el admin aumentó las vidas del nivel y restaura las vidas adicionales
        """
        # Si no tenemos registro de vidas iniciales, establecerlo
        if self.avm_vidas_iniciales_nivel is None:
            self.avm_vidas_iniciales_nivel = self.fk_nivel.niv_vidas
            self.save()
            return 0
        
        # Solo restaurar si el admin AUMENTÓ las vidas del nivel
        if self.fk_nivel.niv_vidas > self.avm_vidas_iniciales_nivel:
            # Calcular cuántas vidas nuevas agregó el admin
            vidas_agregadas_por_admin = self.fk_nivel.niv_vidas - self.avm_vidas_iniciales_nivel
            
            # Agregar esas vidas al estudiante
            self.avm_vidas_restantes += vidas_agregadas_por_admin
            self.avm_vidas_iniciales_nivel = self.fk_nivel.niv_vidas  # Actualizar el registro
            
            # Si estaba sin vidas y ahora tiene vidas, cambiar estado
            if self.avm_estado == 'sin_vidas' and self.avm_vidas_restantes > 0:
                self.avm_estado = 'en_progreso'
            
            self.save()
            return vidas_agregadas_por_admin
        
        return 0

    # MÉTODO ESTÁTICO para restaurar vidas a todos los estudiantes (para usar desde admin)
    @staticmethod
    def restaurar_vidas_todos_estudiantes(nivel_id, vidas_anteriores, vidas_nuevas):
        """
        Restaura vidas a todos los estudiantes cuando el admin aumenta las vidas de un nivel
        """
        if vidas_nuevas > vidas_anteriores:
            vidas_adicionales = vidas_nuevas - vidas_anteriores
            
            # Obtener todos los avances de estudiantes para este nivel
            avances = Avance_Matriculados.objects.filter(fk_nivel_id=nivel_id)
            
            for avance in avances:
                # Solo agregar vidas adicionales, no restaurar las perdidas
                avance.avm_vidas_restantes += vidas_adicionales
                
                if avance.avm_estado == 'sin_vidas' and avance.avm_vidas_restantes > 0:
                    avance.avm_estado = 'en_progreso'
                
                avance.save()
            
            return f"Se agregaron {vidas_adicionales} vidas a {avances.count()} estudiantes"
        
        return "No se agregaron vidas"