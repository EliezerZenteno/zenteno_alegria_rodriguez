from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Posteo(models.Model):
    titulo = models.CharField(max_length=200)
    contenido = models.TextField()
    autor = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    fecha_creacion = models.DateTimeField(default=timezone.now)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    activo = models.BooleanField(default=True)

    class Meta:
        ordering = ['-fecha_creacion']
        verbose_name = 'Posteo'
        verbose_name_plural = 'Posteos'

    def __str__(self):
        return self.titulo
