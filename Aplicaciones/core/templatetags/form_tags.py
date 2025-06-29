from django import template

register = template.Library()

@register.filter(name='add_class')
def add_class(field, css_class):
    try:
        # Solo si es un campo de formulario
        if hasattr(field, 'errors'):
            if field.errors:
                css_class += ' is-invalid'  # Agrega clase Bootstrap de error
            existing_classes = field.field.widget.attrs.get('class', '')
            new_classes = f'{existing_classes} {css_class}'.strip()
            return field.as_widget(attrs={'class': new_classes})
        else:
            return field  # Si es string, lo dejamos igual
    except Exception as e:
        print(f'Error en filtro add_class: {e}')
        return field
