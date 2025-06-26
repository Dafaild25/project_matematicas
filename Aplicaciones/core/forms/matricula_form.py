from django import forms
from ..models import Matriculas, Estudiantes, Clases

class MatriculasForm(forms.ModelForm):
    class Meta:
        model = Matriculas
        fields = ['fk_estudiante', 'fk_clase', 'mat_estado']
        widgets = {
            'fk_estudiante': forms.Select(attrs={'class': 'form-select'}),
            'fk_clase': forms.Select(attrs={'class': 'form-select'}),
            'mat_estado': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super(MatriculasForm, self).__init__(*args, **kwargs)
        # Puedes filtrar estudiantes o clases activas aquí si deseas
        self.fields['fk_estudiante'].queryset = Estudiantes.objects.all()
        self.fields['fk_clase'].queryset = Clases.objects.filter(cla_estado=True)