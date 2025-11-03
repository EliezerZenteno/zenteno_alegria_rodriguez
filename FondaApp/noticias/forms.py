from django import forms
from .models import Posteo, Comentario


class PosteoForm(forms.ModelForm):
    class Meta:
        model = Posteo
        fields = ['titulo', 'contenido']
        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingresa el título de la noticia'
            }),
            'contenido': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 6,
                'placeholder': 'Escribe el contenido de la noticia aquí...'
            }),
        }
        labels = {
            'titulo': 'Título',
            'contenido': 'Contenido',
        }


class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['contenido']
        widgets = {
            'contenido': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Escribe tu comentario aquí...'
            }),
        }
        labels = {
            'contenido': 'Comentario',
        }
