from django.db import models


class Contacto(models.Model):
    """Modelo para almacenar mensajes de contacto"""
    nombre = models.CharField(max_length=100, verbose_name='Nombre')
    email = models.EmailField(verbose_name='Correo electrónico')
    asunto = models.CharField(max_length=200, verbose_name='Asunto')
    mensaje = models.TextField(verbose_name='Mensaje')
    telefono = models.CharField(max_length=20, blank=True, null=True, verbose_name='Teléfono')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de envío')
    leido = models.BooleanField(default=False, verbose_name='Leído')
    
    class Meta:
        ordering = ['-created']
        verbose_name = 'Mensaje de Contacto'
        verbose_name_plural = 'Mensajes de Contacto'
    
    def __str__(self):
        return f'{self.nombre} - {self.asunto}'
