from django import forms
from django.forms import modelformset_factory, inlineformset_factory
from ..models import Enunciados, Preguntas, Opciones, Modulos, Niveles


class EnunciadoForm(forms.ModelForm):
    fk_modulo = forms.ModelChoiceField(
        queryset=Modulos.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="Módulo",
        required=True
    )

    class Meta:
        model = Enunciados
        fields = ['fk_modulo', 'fk_nivel', 'enun_nombre', 'enum_puntaje']
        widgets = {
            'fk_nivel': forms.Select(attrs={'class': 'form-select'}),
            'enun_nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'enum_puntaje': forms.NumberInput(attrs={
                'class': 'form-control',
                'min':0,
                'max':10,
                'step':'0.01',
                'placeholder':'Puntaje entre 0.00 y 10.00'
            }),
        }
    
    def clean_enum_puntaje(self):
        puntaje = self.cleaned_data.get('enum_puntaje')
        if puntaje < 0 or puntaje > 10:
            raise forms.ValidationError('El puntaje debe estar entre 0 y 10.')
        return puntaje

    def __init__(self, *args, **kwargs):
        data = kwargs.get('data')
        super().__init__(*args, **kwargs)
        
        if data and 'fk_modulo' in data:
            try:
                modulo_id = int(data.get('fk_modulo'))
                self.fields['fk_nivel'].queryset = Niveles.objects.filter(fk_modulo_id=modulo_id)
            except (ValueError, TypeError):
                self.fields['fk_nivel'].queryset = Niveles.objects.none()
        elif self.instance.pk:
            self.fields['fk_nivel'].queryset = Niveles.objects.filter(fk_modulo=self.instance.fk_nivel.fk_modulo)
        else:
            self.fields['fk_nivel'].queryset = Niveles.objects.none()


class PreguntaForm(forms.ModelForm):
    class Meta:
        model = Preguntas
        fields = ['pre_nombre', 'pre_tiene_imagen', 'pre_imagen']
        widgets = {
            'pre_nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese una pregunta'}),
            'pre_tiene_imagen': forms.CheckboxInput(attrs={'class': 'form-check-input toggle-imagen'}),
            'pre_imagen': forms.ClearableFileInput(attrs={'class': 'form-control imagen-field', 'style': 'display:none;'}),
        }


class OpcionForm(forms.ModelForm):
    class Meta:
        model = Opciones
        fields = ['op_nombre', 'op_correcta']
        widgets = {
            'op_nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'op_correcta': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

# Un Formset de opciones para cada pregunta (mínimo 2, máximo 10 opciones por pregunta)
OpcionFormSet = modelformset_factory(
    Opciones,
    form=OpcionForm,
    extra=1,
    can_delete=True,
    min_num=2,
    max_num=10,
    validate_min=True,
    validate_max=True
)

# Un InlineFormSet para enlazar muchas preguntas a un enunciado
PreguntaFormSet = inlineformset_factory(
    Enunciados,
    Preguntas,
    form=PreguntaForm,
    extra=1,
    can_delete=False
)
