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
    per_edad = models.IntegerField(default=0,verbose_name="Edad:")
    per_cedula = models.CharField(max_length=15,default="Null",null=False,verbose_name="Cédula:")
    per_fecha_nacimiento = models.DateField(default="Null",verbose_name="Fecha de nacimiento:")
    per_telefono = models.CharField(max_length=15,default="Null",null=True,verbose_name="Teléfono:")
    per_fecha_actualizacion = models.DateTimeField(auto_now=True,verbose_name='Actualizado el:')
    # Mejorar presentacion de los datos
    def __str__(self):
        # Obtener grupo al que pertenece
        grupo = self.id_fk_usuario.groups.first()
        nombre_grupo = grupo.name
        nombre_grupo = grupo.name if grupo else "Sin grupo definido" # Validar que exita en un grupo

        fila = "{0}: {1} {2} - {3}" # Debo mostrar el grupo al que pertenece
        return fila.format(self.per_id,self.fk_id_usuario.first_name,self.fk_id_usuario.last_name,nombre_grupo)
    
# MODULO ADMINISTRADORES
class Administradores(models.Model):
    adm_id = models.AutoField(primary_key=True)
    # Clave foranea Persona
    fk_id_persona = models.ForeignKey(Personas,verbose_name='Persona',on_delete=models.CASCADE)
    adm_estado = models.BooleanField(default=True,verbose_name='Estado:')
    adm_fecha_creacion = models.DateTimeField(default=timezone.now,verbose_name='Fecha de creación:')
    adm_fecha_actualizacion = models.DateTimeField(auto_now=True,verbose_name='Actualizado el:')
    
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
    doc_fecha_actualizacion = models.DateTimeField(auto_now=True,verbose_name='Actualizado el:')
    
    def __str__(self):
        return f"{self.doc_id}: {self.fk_id_persona.fk_id_usuario.first_name} {self.fk_id_persona.fk_id_usuario.last_name}"
    
# MODULO ESTUDIANTES
class Estudiantes(models.Model):
    est_id = models.AutoField(primary_key=True)
    # Clave foranea Persona
    fk_id_persona = models.ForeignKey(Personas,verbose_name='Persona',on_delete=models.CASCADE)
    est_fotografia = models.ImageField(upload_to='estudiantes/',default='Sin Foto',null=True,blank=True,verbose_name="Fotografía:")
    est_contacto_emergencia = models.CharField(max_length=50,default="Null",null=True,verbose_name="Contacto de emergencia:")
    est_telefono_emergencia = models.CharField(max_length=15,default="Null",null=True,verbose_name="Teléfono de emergencia:")
    est_estado = models.BooleanField(default=True,verbose_name='Estado:')
    est_fecha_actualizacion = models.DateTimeField(auto_now=True,verbose_name='Actualizado el:')
    def __str__(self):
        return f"{self.est_id}: {self.fk_id_persona.fk_id_usuario.first_name} {self.fk_id_persona.fk_id_usuario.last_name}"