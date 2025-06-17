from django import forms
from ..models import Modulos


class ModulosForm(forms.ModelForm):
    class Meta:
        model = Modulos
        fields = ['mod_nombre', 'mod_descripcion', 'mod_estado']
        widgets = {
            'mod_nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'mod_descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'mod_estado': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean_mod_nombre(self):
        nombre = self.cleaned_data.get('mod_nombre')
        if not nombre:
            raise forms.ValidationError('El nombre del módulo es obligatorio.')

        # Evitar duplicado al crear
        if self.instance.pk:
            # Estamos editando: excluir el actual
            if Modulos.objects.exclude(pk=self.instance.pk).filter(mod_nombre__iexact=nombre).exists():
                raise forms.ValidationError('Ya existe un módulo con este nombre.')
        else:
            # Estamos creando
            if Modulos.objects.filter(mod_nombre__iexact=nombre).exists():
                raise forms.ValidationError('Ya existe un módulo con este nombre.')

        return nombre

