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
        return f" {self.fk_id_persona.fk_id_usuario.first_name} {self.fk_id_persona.fk_id_usuario.last_name}"
    
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
    niv_nombre = models.CharField(max_length=50, null=False, verbose_name="Nombre del nivel:")
    niv_descripcion = models.CharField(max_length=100,null=False,verbose_name="Descripción del nivel:")
    orden = models.IntegerField()
    vidas = models.IntegerField()
    ruta = models.CharField(max_length=100,null=True,verbose_name="Ruta:")
    niv_estado = models.BooleanField(default=True,verbose_name='Estado:')
    niv_fecha_creacion = models.DateTimeField(auto_now_add=True,verbose_name='Creado el:')
    niv_fecha_actualizacion = models.DateTimeField(auto_now=True,verbose_name='Actualizado el:')
    
    def __str__(self):
        return f"{self.niv_id}: {self.niv_nombre}"
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['fk_modulo', 'niv_nombre'], name='unique_nombre_por_modulo')
        ]

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


##Ignoraremos  enunciados  preguntas y opciones
class Enunciados(models.Model):
    enun_id = models.AutoField(primary_key=True)
    fk_nivel = models.ForeignKey(Niveles,verbose_name='Nivel',on_delete=models.CASCADE)
    enun_nombre = models.CharField(max_length=100,null=False,verbose_name="Enunciado:")
    enum_puntaje = models.DecimalField(max_digits=5,decimal_places=2,null=False,verbose_name="Puntaje:")
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
    


# Modulo de  Matriculas

class Matriculas(models.Model):
    mat_id = models.AutoField(primary_key=True)
    fk_estudiante = models.ForeignKey(Estudiantes,verbose_name='Estudiante',on_delete=models.CASCADE)
    fk_clase = models.ForeignKey(Clases,verbose_name='Clase',on_delete=models.CASCADE)
    mat_estado = models.BooleanField(default=True,verbose_name='Estado:')
    mat_fecha_creacion = models.DateTimeField(auto_now_add=True,verbose_name='Creado el:')
    mat_fecha_actualizacion = models.DateTimeField(auto_now=True,verbose_name='Actualizado el:')
