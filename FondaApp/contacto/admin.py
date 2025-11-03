from django.contrib import admin
from django.utils.html import format_html
from .models import Contacto


@admin.register(Contacto)
class ContactoAdmin(admin.ModelAdmin):
    """Admin personalizado para Contacto"""
    list_display = ['nombre', 'email', 'asunto', 'telefono', 'leido_badge', 'leido', 'created']
    list_filter = ['leido', 'created']
    search_fields = ['nombre', 'email', 'asunto', 'mensaje']
    list_editable = ['leido']
    date_hierarchy = 'created'
    ordering = ['-created']
    readonly_fields = ['created']
    
    fieldsets = (
        ('Información del contacto', {
            'fields': ('nombre', 'email', 'telefono')
        }),
        ('Mensaje', {
            'fields': ('asunto', 'mensaje')
        }),
        ('Estado', {
            'fields': ('leido', 'created'),
        }),
    )
    
    actions = ['marcar_leido', 'marcar_no_leido']
    
    def leido_badge(self, obj):
        """Mostrar badge de estado leído"""
        if obj.leido:
            return format_html(
                '<span style="background-color: #28a745; color: white; padding: 3px 10px; border-radius: 3px;">✓ Leído</span>'
            )
        return format_html(
            '<span style="background-color: #dc3545; color: white; padding: 3px 10px; border-radius: 3px;">✗ No leído</span>'
        )
    leido_badge.short_description = 'Estado'
    
    def marcar_leido(self, request, queryset):
        """Acción para marcar como leído"""
        updated = queryset.update(leido=True)
        self.message_user(request, f'{updated} mensaje(s) marcado(s) como leído(s).')
    marcar_leido.short_description = 'Marcar como leído'
    
    def marcar_no_leido(self, request, queryset):
        """Acción para marcar como no leído"""
        updated = queryset.update(leido=False)
        self.message_user(request, f'{updated} mensaje(s) marcado(s) como no leído(s).')
    marcar_no_leido.short_description = 'Marcar como no leído'
