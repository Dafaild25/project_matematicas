from django.db import models


# models.py
class Persona(models.Model):
    nombres = models.CharField(max_length=255)
    apellidos = models.CharField(max_length=255)
    dni = models.BooleanField()
    email = models.EmailField()

class Usuario(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE)
    estado = models.CharField(max_length=15)

class Administrador(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)