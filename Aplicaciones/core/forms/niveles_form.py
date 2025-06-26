from django import forms
from ..models import Niveles

class NivelesForm(forms.ModelForm):
    class Meta:
        model = Niveles
        fields = ['fk_modulo', 'niv_nombre', 'niv_descripcion', 'orden', 'vidas','ruta']
        widgets = {
            'fk_modulo': forms.Select(attrs={'class': 'form-select'}),
            'niv_nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'niv_descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'orden': forms.NumberInput(attrs={'class': 'form-control', 'min':1,'max':10}),
            'vidas': forms.NumberInput(attrs={'class': 'form-control', 'min':1,'max':10}),
            'ruta': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_niv_nombre(self):
        nombre = self.cleaned_data.get('niv_nombre')
        modulo = self.cleaned_data.get('fk_modulo')

        if not nombre or not modulo:
            return nombre
        qs = Niveles.objects.filter(fk_modulo=modulo, niv_nombre__iexact=nombre)    

        # Validación de unicidad (aunque el modelo ya lo impone)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
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