from django import forms # Importar modelo de formularios
from django.contrib.auth.forms import UserCreationForm # Importar modelo para crear formulario
from django.contrib.auth.models import User # Importar clase User
from django.core.validators import RegexValidator,MinLengthValidator # Importar modelo para validaciones
from django.core.exceptions import ValidationError # Importar modelo de validación de errores
from django.utils import timezone # Importar modelo de zona horaria
from datetime import date # Importar modelo de fecha
import re # Importar expresiones regulares para validaciones

# VALIDACIONES DE FORMULARIO PARA CREAR USUARIOS
class UserCreateForm(UserCreationForm):
    first_name = forms.CharField(
        label='Nombre',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su nombre'}),
        validators=[
            MinLengthValidator(2, 'Su nombre es muy corto'),
            RegexValidator('^[A-Za-ñÑáéíóúÁÉÍÓÚ ]+$', 'No incluir datos especiales ni números'),
        ]
    )
    last_name = forms.CharField(
        label='Primer Apellido',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese solo un apellido'}),
        validators=[
            MinLengthValidator(2, 'Su apellido es muy corto'),
            RegexValidator('^[A-Za-ñÑáéíóúÁÉÍÓÚ ]+$', 'No incluir datos especiales ni números'),
        ]
    )
    email = forms.EmailField(
        label='Correo Electrónico',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'ejemplo@gmail.com'}),
        error_messages={
            'invalid': 'Ingrese un correo electrónico válido (ej: ejemplo@gmail.com).'
        }
    )
    password1 = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su contraseña'}),
        error_messages={
            'required': 'Este campo es obligatorio.'
        }
    )
    password2 = forms.CharField(
        label='Confirmar Contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirme su contraseña'}),
        error_messages={
            'required': 'Este campo es obligatorio.'
        }
    )
    # Validar correo electrónico
    def clean_email(self):
        email = self.cleaned_data.get('email')
        dominios_validos = ['gmail.com', 'hotmail.com', 'outlook.com', 'yahoo.com']
        if email:
            dominio = email.split('@')[-1]
            if dominio.lower() not in dominios_validos:
                raise ValidationError('El correo debe ser de gmail, hotmail, outlook o yahoo.')
            if User.objects.filter(email=email).exists():
                raise ValidationError('Este correo ya está registrado.')
        return email
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese un nombre de usuario'}),
        }

# VALIDACIONES DE FORMULARIO PARA ACTUALIZAR USUARIOS
class UserUpdateForm(forms.ModelForm):
    first_name = forms.CharField(
        label='Nombre',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su nombre'}),
        validators=[
            MinLengthValidator(2, 'Su nombre es muy corto'),
            RegexValidator('^[A-Za-ñÑáéíóúÁÉÍÓÚ ]+$', 'No incluir datos especiales ni números'),
        ]
    )
    last_name = forms.CharField(
        label='Primer Apellido',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese solo un apellido'}),
        validators=[
            MinLengthValidator(2, 'Su apellido es muy corto'),
            RegexValidator('^[A-Za-ñÑáéíóúÁÉÍÓÚ ]+$', 'No incluir datos especiales ni números'),
        ]
    )
    email = forms.EmailField(
        label='Correo Electrónico',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'ejemplo@gmail.com'}),
        error_messages={
            'invalid': 'Ingrese un correo electrónico válido (ej: ejemplo@gmail.com).'
        }
    )  
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese un nombre de usuario'}),
        }
    # Validar email cuando cambie
    def clean_email(self):
        email = self.cleaned_data.get('email')
        dominios_validos = ['gmail.com', 'hotmail.com', 'outlook.com', 'yahoo.com']
        if email:
            dominio = email.split('@')[-1]
            if dominio.lower() not in dominios_validos:
                raise ValidationError('El correo debe ser de gmail, hotmail, outlook o yahoo.')
            if self.instance and email != self.instance.email:
                if User.objects.filter(email=email).exists():
                    raise ValidationError('Este correo ya está registrado.')
        return email
    # Validar username cuando cambie
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if self.instance and username != self.instance.username:
            if User.objects.filter(username=username).exists():
                raise ValidationError('Este nombre de usuario ya está registrado.')
        return username


# VALIDACIONES DE FORMULARIO PARA CREAR PERSONAS
class PersonaCreateForm(forms.Form):
    per_segundo_nombre = forms.CharField(
        label='Segundo Nombre',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su segundo nombre'}),
        validators=[
            MinLengthValidator(2, 'El nombre es muy corto.'),
            RegexValidator('^[A-Za-zñÑ ]+$', 'El nombre no puede tener caracteres especiales ni números.')
        ]
    )
    per_segundo_apellido = forms.CharField(
        label='Segundo Apellido',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su segundo apellido'}),
        validators=[
            MinLengthValidator(2, 'El apellido es muy corto.'),
            RegexValidator('^[A-Za-zñÑ ]+$', 'El apellido no puede tener caracteres especiales ni números.')
        ]
    )
    per_fecha_nacimiento = forms.DateField(
        label='Fecha de Nacimiento',
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    cedula = forms.CharField(
        label='Cédula',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su número de cédula'}),
        min_length=10,
        max_length=10
    )
    per_telefono = forms.CharField(
        label='Teléfono',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su número de teléfono'}),
        max_length=10,
        validators=[
            RegexValidator('^[0-9]+$', 'El teléfono solo debe contener números.')
        ]
    )
    # Validaciones de numero de teléfono
    def clean_per_telefono(self):
        telefono = self.cleaned_data['per_telefono']
        if not telefono.isdigit():
            raise ValidationError("El teléfono solo debe contener números.")
        if len(telefono) != 10:
            raise ValidationError("El número de celular debe tener exactamente 10 dígitos.")
        if not telefono.startswith('09'):
            raise ValidationError("El número de celular debe comenzar con '09'.")
        return telefono
    
    # Limpiar campo de cedula
    def clean_cedula(self):
        cedula = self.cleaned_data['cedula']
        if not self.validar_cedula_ecuatoriana(cedula):
            raise forms.ValidationError('Cédula inválida.')
        return cedula
    
    # Validar fecha de nacimiento
    def clean_per_fecha_nacimiento(self):
        fecha = self.cleaned_data['per_fecha_nacimiento']
        hoy = date.today()
        edad_minima = 5
        edad_maxima = 120
        if fecha > hoy:
            raise forms.ValidationError("La fecha de nacimiento no puede ser en el futuro.") 
        edad = hoy.year - fecha.year - ((hoy.month, hoy.day) < (fecha.month, fecha.day))
        if edad < edad_minima:
            raise forms.ValidationError(f"La edad mínima permitida es {edad_minima} años.")
        if edad > edad_maxima:
            raise forms.ValidationError(f"La edad máxima permitida es {edad_maxima} años.")
        return fecha

    # Validar cédula ecuatoriana
    def validar_cedula_ecuatoriana(self, cedula):
        if len(cedula) != 10 or not cedula.isdigit():
            return False
        provincia = int(cedula[0:2])
        if provincia < 1 or provincia > 24:
            return False
        digitos = list(map(int, cedula))
        suma = 0
        for i in range(9):
            if i % 2 == 0:
                valor = digitos[i] * 2
                if valor > 9:
                    valor -= 9
            else:
                valor = digitos[i]
            suma += valor
        verificador = 10 - (suma % 10)
        if verificador == 10:
            verificador = 0
        return verificador == digitos[9]
 