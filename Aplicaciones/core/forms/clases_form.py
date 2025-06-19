from django import forms 

from ..models import Clases, Docentes, Modulos

class ClasesForm(forms.ModelForm):
    class Meta:
        model = Clases
        fields = ['fk_docente','fk_modulo']
        widgets ={
            'fk_docente': forms.Select(attrs={'class': 'form-select'}),
            'fk_modulo': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super(ClasesForm, self).__init__(*args, **kwargs)
        self.fields['fk_docente'].queryset = Docentes.objects.filter(doc_estado=True)
        self.fields['fk_modulo'].queryset = Modulos.objects.filter(mod_estado=True)
        
        if not self.instance.pk:
            self.instance.cla_estado = True