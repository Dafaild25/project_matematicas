from django import forms 

from ..models import Clases, Docentes, Modulos

class ClasesForm(forms.ModelForm):
    class Meta:
        model = Clases
        fields = ['fk_docente','fk_modulo','cla_nombre']
        widgets ={
            'fk_docente': forms.Select(attrs={'class': 'form-select'}),
            'fk_modulo': forms.Select(attrs={'class': 'form-select'}),
            'cla_nombre': forms.TextInput(attrs={'class': 'form-control','required': 'required'}),
        }

    def __init__(self, *args, **kwargs):
        super(ClasesForm, self).__init__(*args, **kwargs)
        self.fields['fk_docente'].queryset = Docentes.objects.filter(doc_estado=True)
        self.fields['fk_modulo'].queryset = Modulos.objects.filter(mod_estado=True)
        
        if not self.instance.pk:
            self.instance.cla_estado = True
            
    def clean_cla_nombre(self):
        nombre = self.cleaned_data.get('cla_nombre')
        modulo = self.cleaned_data.get('fk_modulo')
        

        if not nombre or not modulo:
            return nombre
        qs = Clases.objects.filter(fk_modulo=modulo, cla_nombre__iexact=nombre)    

        # Validación de unicidad (aunque el modelo ya lo impone)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError('Ya existe una clase con este nombre.')

        return nombre