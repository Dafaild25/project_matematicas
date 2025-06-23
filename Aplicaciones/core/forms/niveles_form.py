from django import forms
from ..models import Niveles

class NivelesForm(forms.ModelForm):
    class Meta:
        model = Niveles
        fields = ['fk_modulo', 'niv_nombre', 'niv_descripcion', 'orden', 'vidas']
        widgets = {
            'fk_modulo': forms.Select(attrs={'class': 'form-select'}),
            'niv_nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'niv_descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'orden': forms.NumberInput(attrs={'class': 'form-control', 'min':1,'max':10}),
            'vidas': forms.NumberInput(attrs={'class': 'form-control', 'min':1,'max':10}),
        }

    def clean_niv_nombre(self):
        nombre = self.cleaned_data.get('niv_nombre')

        if not nombre:
            raise forms.ValidationError('El nombre del nivel es obligatorio.')

        # Validación de unicidad (aunque el modelo ya lo impone)
        if self.instance.pk:
            if Niveles.objects.exclude(pk=self.instance.pk).filter(niv_nombre__iexact=nombre).exists():
                raise forms.ValidationError('Ya existe un nivel con este nombre.')
        else:
            if Niveles.objects.filter(niv_nombre__iexact=nombre).exists():
                raise forms.ValidationError('Ya existe un nivel con este nombre.')

        return nombre
    def clean_orden(self):
        orden = self.cleaned_data.get('orden')
        if orden < 1 or orden > 10:
            raise forms.ValidationError('El orden debe estar entre 1 y 10.')
        return orden

    def clean_vidas(self):
        vidas = self.cleaned_data.get('vidas')
        if vidas < 1 or vidas > 10:
            raise forms.ValidationError('Las vidas deben estar entre 1 y 10.')
        return vidas
