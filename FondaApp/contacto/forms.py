from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Field
from .models import Contacto


class ContactoForm(forms.ModelForm):
    """Formulario de contacto con crispy forms"""
    
    class Meta:
        model = Contacto
        fields = ['nombre', 'email', 'telefono', 'asunto', 'mensaje']
        widgets = {
            'mensaje': forms.Textarea(attrs={'rows': 5}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-3'
        self.helper.field_class = 'col-lg-9'
        
        # Layout del formulario
        self.helper.layout = Layout(
            Row(
                Column('nombre', css_class='form-group col-md-6 mb-3'),
                Column('email', css_class='form-group col-md-6 mb-3'),
                css_class='form-row'
            ),
            Row(
                Column('telefono', css_class='form-group col-md-6 mb-3'),
                Column('asunto', css_class='form-group col-md-6 mb-3'),
                css_class='form-row'
            ),
            Field('mensaje', css_class='mb-3'),
            Submit('submit', 'Enviar Mensaje', css_class='btn btn-primary btn-lg btn-block')
        )
        
        # Placeholders
        self.fields['nombre'].widget.attrs.update({'placeholder': 'Tu nombre completo'})
        self.fields['email'].widget.attrs.update({'placeholder': 'tu@email.com'})
        self.fields['telefono'].widget.attrs.update({'placeholder': '+56 9 1234 5678'})
        self.fields['asunto'].widget.attrs.update({'placeholder': 'Asunto del mensaje'})
        self.fields['mensaje'].widget.attrs.update({'placeholder': 'Escribe tu mensaje aquí...'})
