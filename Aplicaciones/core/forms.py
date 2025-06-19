from django import forms # Importar modelo de formularios
from django.core import validators # Importar modelo para validaciones

from django.contrib.auth.forms import UserCreationForm # Importar modelo para crear formulario
from django.contrib.auth.models import User # Importar clase User

class UserForm(UserCreationForm):
    first_name = forms.CharField(
        label='Nombre',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su nombre'}),
        validators=[
            validators.MinLengthValidator(2, 'Su nombre es muy corto'), # Numero minimo de caracteres
            validators.RegexValidator('^[A-Za-ñ ]+$', 'No incluir datos especiales'), # Aceptar un cierto tipo de caracteres
        ]
    )
    last_name = forms.CharField(
        label='Primer Apellido',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese solo un apellido'}),
        validators=[
            validators.MinLengthValidator(2, 'Su apellido es muy corto'), # Numero minimo de caracteres
            validators.RegexValidator('^[A-Za-ñ ]+$', 'No incluir datos especiales'), # Aceptar un cierto tipo de caracteres
        ]
    )
    email = forms.EmailField(
        label='Correo Electrónico',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'ejemplo@ejemplo.com'}),
        required=False
    )
    password1 = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su contraseña'})
    )
    password2 = forms.CharField(
        label='Confirmar Contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirme su contraseña'})
    )
    class Meta:
        model = User # modelo basado en USer
        fields = ['first_name','last_name','email','username','password1','password2'] # Campos Clase User
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su nombre'}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese un nombre de usuario'}),
        }