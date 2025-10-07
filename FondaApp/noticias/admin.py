from django.contrib import admin
from .models import Posteo


@admin.register(Posteo)
class PosteoAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'autor', 'fecha_creacion', 'activo']
    list_filter = ['activo', 'fecha_creacion', 'autor']
    search_fields = ['titulo', 'contenido', 'autor__username']
    list_editable = ['activo']
    date_hierarchy = 'fecha_creacion'
    ordering = ['-fecha_creacion']
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion']
    
    fieldsets = (
        ('Información básica', {
            'fields': ('titulo', 'contenido', 'autor')
        }),
        ('Estado y fechas', {
            'fields': ('activo', 'fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )
    
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
