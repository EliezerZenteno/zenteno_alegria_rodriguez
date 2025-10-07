from django.contrib import admin
from django.utils.html import format_html
from .models import Posteo


@admin.register(Posteo)
class PosteoAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'autor', 'imagen_thumbnail', 'created', 'activo']
    list_filter = ['activo', 'created', 'autor']
    search_fields = ['titulo', 'contenido', 'autor__username']
    list_editable = ['activo']
    date_hierarchy = 'created'
    ordering = ['-created']
    readonly_fields = ['created', 'updated', 'imagen_preview']
    
    fieldsets = (
        ('Información básica', {
            'fields': ('titulo', 'contenido', 'imagen', 'imagen_preview', 'autor')
        }),
        ('Estado y fechas', {
            'fields': ('activo', 'created', 'updated'),
            'classes': ('collapse',)
        }),
    )
    
    def imagen_thumbnail(self, obj):
        """Mostrar thumbnail de la imagen en la lista"""
        if obj.imagen:
            return format_html(
                '<img src="{}" width="50" height="50" style="object-fit: cover; border-radius: 4px;" />',
                obj.imagen.url
            )
        return "Sin imagen"
    imagen_thumbnail.short_description = 'Imagen'
    
    def imagen_preview(self, obj):
        """Mostrar preview de la imagen en el formulario"""
        if obj.imagen:
            return format_html(
                '<img src="{}" width="200" style="border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);" />',
                obj.imagen.url
            )
        return "No hay imagen subida"
    imagen_preview.short_description = 'Vista previa'
    
    def save_model(self, request, obj, form, change):
        # Si es una nueva noticia, asignar el usuario actual como autor
        if not change and not obj.autor_id:
            obj.autor = request.user
        super().save_model(request, obj, form, change)
    
    # Personalizar la vista de lista
    list_per_page = 20
    
    # Filtros laterales más útiles
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Los usuarios normales solo ven sus propias noticias
        # Los staff ven todas las noticias
        if request.user.is_superuser:
            return qs
        return qs.filter(autor=request.user)
