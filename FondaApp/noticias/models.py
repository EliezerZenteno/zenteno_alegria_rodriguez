from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Posteo(models.Model):
    titulo = models.CharField(max_length=200, verbose_name='Título')
    contenido = models.TextField(verbose_name='Contenido')
    imagen = models.ImageField(
        upload_to='noticias/', 
        blank=True, 
        null=True, 
        verbose_name='Imagen',
        help_text='Imagen opcional para la noticia'
    )
    autor = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        default=1,
        verbose_name='Autor'
    )
    created = models.DateTimeField(
        auto_now_add=True, 
        verbose_name='Fecha de creación'
    )
    updated = models.DateTimeField(
        auto_now=True, 
        verbose_name='Fecha de actualización'
    )
    activo = models.BooleanField(default=True, verbose_name='Activo')

    class Meta:
        ordering = ['-created']
        verbose_name = 'Posteo'
        verbose_name_plural = 'Posteos'

    def __str__(self):
        return self.titulo
