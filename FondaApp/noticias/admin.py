from django.contrib import admin
from django.utils.html import format_html
from .models import Posteo, Categoria, Comentario


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    """Admin personalizado para Categoría"""
    list_display = ['nombre', 'slug', 'activo', 'orden', 'total_posteos', 'created']
    list_filter = ['activo', 'created']
    search_fields = ['nombre', 'descripcion']
    list_editable = ['activo', 'orden']
    prepopulated_fields = {'slug': ('nombre',)}
    ordering = ['orden', 'nombre']
    
    def total_posteos(self, obj):
        """Mostrar total de posteos en la categoría"""
        count = obj.posteos.count()
        return format_html('<strong>{}</strong>', count)
    total_posteos.short_description = 'Total Posteos'


class ComentarioInline(admin.TabularInline):
    """Inline para mostrar comentarios en el admin de Posteo"""
    model = Comentario
    extra = 0
    fields = ['autor', 'contenido', 'activo', 'created']
    readonly_fields = ['created']
    can_delete = True


@admin.register(Posteo)
class PosteoAdmin(admin.ModelAdmin):
    """Admin personalizado para Posteo con más de 5 parámetros"""
    # 1. list_display - Define las columnas a mostrar en la lista
    list_display = ['titulo', 'categoria', 'autor', 'imagen_thumbnail', 'destacado', 'total_comentarios_display', 'visitas', 'created', 'activo']
    
    # 2. list_filter - Filtros laterales
    list_filter = ['activo', 'destacado', 'categoria', 'created', 'autor']
    
    # 3. search_fields - Campos de búsqueda
    search_fields = ['titulo', 'contenido', 'autor__username', 'categoria__nombre']
    
    # 4. list_editable - Campos editables desde la lista
    list_editable = ['activo', 'destacado']
    
    # 5. date_hierarchy - Navegación por fechas
    date_hierarchy = 'created'
    
    # 6. ordering - Orden por defecto
    ordering = ['-created', '-destacado']
    
    # 7. readonly_fields - Campos de solo lectura
    readonly_fields = ['created', 'updated', 'imagen_preview', 'visitas']
    
    # 8. fieldsets - Organización del formulario
    fieldsets = (
        ('Información básica', {
            'fields': ('titulo', 'contenido', 'categoria', 'autor')
        }),
        ('Multimedia', {
            'fields': ('imagen', 'imagen_preview'),
        }),
        ('Estado y opciones', {
            'fields': ('activo', 'destacado', 'visitas'),
        }),
        ('Fechas', {
            'fields': ('created', 'updated'),
            'classes': ('collapse',)
        }),
    )
    
    # 9. inlines - Modelos relacionados inline
    inlines = [ComentarioInline]
    
    # 10. list_per_page - Paginación
    list_per_page = 20
    
    # 11. actions - Acciones personalizadas
    actions = ['marcar_destacado', 'desmarcar_destacado', 'activar_posteos', 'desactivar_posteos']
    
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
                '<img src="{}" width="300" style="border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);" />',
                obj.imagen.url
            )
        return "No hay imagen subida"
    imagen_preview.short_description = 'Vista previa'
    
    def total_comentarios_display(self, obj):
        """Mostrar total de comentarios"""
        return obj.total_comentarios()
    total_comentarios_display.short_description = 'Comentarios'
    
    def marcar_destacado(self, request, queryset):
        """Acción para marcar posteos como destacados"""
        updated = queryset.update(destacado=True)
        self.message_user(request, f'{updated} posteo(s) marcado(s) como destacado(s).')
    marcar_destacado.short_description = 'Marcar como destacado'
    
    def desmarcar_destacado(self, request, queryset):
        """Acción para desmarcar posteos destacados"""
        updated = queryset.update(destacado=False)
        self.message_user(request, f'{updated} posteo(s) desmarcado(s) como destacado(s).')
    desmarcar_destacado.short_description = 'Desmarcar como destacado'
    
    def activar_posteos(self, request, queryset):
        """Acción para activar posteos"""
        updated = queryset.update(activo=True)
        self.message_user(request, f'{updated} posteo(s) activado(s).')
    activar_posteos.short_description = 'Activar posteos seleccionados'
    
    def desactivar_posteos(self, request, queryset):
        """Acción para desactivar posteos"""
        updated = queryset.update(activo=False)
        self.message_user(request, f'{updated} posteo(s) desactivado(s).')
    desactivar_posteos.short_description = 'Desactivar posteos seleccionados'
    
    def save_model(self, request, obj, form, change):
        """Si es una nueva noticia, asignar el usuario actual como autor"""
        if not change and not obj.autor_id:
            obj.autor = request.user
        super().save_model(request, obj, form, change)


@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    """Admin personalizado para Comentario"""
    list_display = ['posteo', 'autor', 'contenido_corto', 'activo', 'created']
    list_filter = ['activo', 'created', 'posteo']
    search_fields = ['contenido', 'autor__username', 'posteo__titulo']
    list_editable = ['activo']
    date_hierarchy = 'created'
    ordering = ['-created']
    readonly_fields = ['created', 'updated']
    
    fieldsets = (
        ('Información', {
            'fields': ('posteo', 'autor', 'contenido')
        }),
        ('Estado', {
            'fields': ('activo', 'created', 'updated'),
        }),
    )
    
    def contenido_corto(self, obj):
        """Mostrar versión corta del contenido"""
        if len(obj.contenido) > 50:
            return f'{obj.contenido[:50]}...'
        return obj.contenido
    contenido_corto.short_description = 'Comentario'
    
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
