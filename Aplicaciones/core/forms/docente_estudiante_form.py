
# archivo: forms.py
from django import forms
from django.contrib.auth.models import User
from ..models import Personas, Estudiantes

class CrearEstudianteForm(forms.Form):
    nombre = forms.CharField(label="Nombre", max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}))
    segundo_nombre = forms.CharField(label="Segundo nombre", max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    apellido = forms.CharField(label="Apellido", max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}))
    segundo_apellido = forms.CharField(label="Segundo apellido", max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="Correo electrónico", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    cedula = forms.CharField(label="Cédula", max_length=15, widget=forms.TextInput(attrs={'class': 'form-control'}))
    telefono = forms.CharField(label="Teléfono", max_length=15, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    fecha_nacimiento = forms.DateField(label="Fecha de nacimiento", required=False, widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))
    contacto_emergencia = forms.CharField(label="Contacto de emergencia", max_length=50, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    telefono_emergencia = forms.CharField(label="Teléfono de emergencia", max_length=15, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    clase_id = forms.IntegerField(widget=forms.HiddenInput())
    password = forms.CharField(
        label="Nueva contraseña (opcional)", 
        widget=forms.PasswordInput(attrs={'class': 'form-control'}), 
        required=False
    )

    
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise forms.ValidationError("El correo es obligatorio.")
        return email

    def clean_cedula(self):
        cedula = self.cleaned_data.get('cedula')
        if not cedula:
            raise forms.ValidationError("La cédula es obligatoria.")
        return cedula