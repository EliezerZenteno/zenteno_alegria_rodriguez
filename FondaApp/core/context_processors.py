"""
Context processors personalizados para FondaApp
"""
from noticias.models import Categoria, Posteo
from django.db.models import Count


def fonda_context(request):
    """
    Context processor personalizado que agrega información global
    disponible en todos los templates
    """
    context = {
        # Categorías activas para el menú
        'categorias_globales': Categoria.objects.filter(activo=True).order_by('orden'),
        
        # Estadísticas generales
        'total_noticias': Posteo.objects.filter(activo=True).count(),
        
        # Noticias destacadas para sidebar
        'noticias_destacadas': Posteo.objects.filter(
            activo=True, 
            destacado=True
        ).order_by('-created')[:3],
        
        # Últimas noticias para footer o sidebar
        'ultimas_noticias': Posteo.objects.filter(
            activo=True
        ).order_by('-created')[:5],
        
        # Categorías con conteo de posteos
        'categorias_con_conteo': Categoria.objects.filter(
            activo=True
        ).annotate(
            total_posteos=Count('posteos', filter=models.Q(posteos__activo=True))
        ).order_by('orden'),
        
        # Información del sitio
        'nombre_sitio': 'FondaApp',
        'año_actual': 2025,
    }
    
    return context


# Necesitamos importar models para el Q
from django.db import models
