from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Categoria(models.Model):
    """Modelo para categorías de noticias"""
    nombre = models.CharField(max_length=100, unique=True, verbose_name='Nombre')
    descripcion = models.TextField(blank=True, verbose_name='Descripción')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='Slug')
    activo = models.BooleanField(default=True, verbose_name='Activo')
    orden = models.IntegerField(default=0, verbose_name='Orden', help_text='Orden de visualización')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    
    class Meta:
        ordering = ['orden', 'nombre']
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'
    
    def __str__(self):
        return self.nombre


class Posteo(models.Model):
    """Modelo para posteos/noticias"""
    titulo = models.CharField(max_length=200, verbose_name='Título')
    contenido = models.TextField(verbose_name='Contenido')
    imagen = models.ImageField(
        upload_to='noticias/', 
        blank=True, 
        null=True, 
        verbose_name='Imagen',
        help_text='Imagen opcional para la noticia'
    )
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='posteos',
        verbose_name='Categoría'
    )
    autor = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        default=1,
        related_name='posteos',
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
    destacado = models.BooleanField(default=False, verbose_name='Destacado')
    visitas = models.IntegerField(default=0, verbose_name='Visitas')

    class Meta:
        ordering = ['-created']
        verbose_name = 'Posteo'
        verbose_name_plural = 'Posteos'

    def __str__(self):
        return self.titulo
    
    def total_comentarios(self):
        """Retorna el total de comentarios activos"""
        return self.comentarios.filter(activo=True).count()


class Comentario(models.Model):
    """Modelo para comentarios en posteos"""
    posteo = models.ForeignKey(
        Posteo,
        on_delete=models.CASCADE,
        related_name='comentarios',
        verbose_name='Posteo'
    )
    autor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comentarios',
        verbose_name='Autor'
    )
    contenido = models.TextField(verbose_name='Comentario')
    activo = models.BooleanField(default=True, verbose_name='Activo')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    updated = models.DateTimeField(auto_now=True, verbose_name='Fecha de actualización')
    
    class Meta:
        ordering = ['-created']
        verbose_name = 'Comentario'
        verbose_name_plural = 'Comentarios'
    
    def __str__(self):
        return f'Comentario de {self.autor.username} en {self.posteo.titulo}'
