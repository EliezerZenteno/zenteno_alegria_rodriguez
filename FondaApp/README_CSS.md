# Estructura de Archivos Estáticos - FondaApp

## Organización de CSS

La aplicación ahora utiliza archivos CSS externos organizados en la carpeta `static/css/`:

### Archivos principales:

1. **`base.css`** - Estilos base compartidos por toda la aplicación
   - Navegación
   - Footer
   - Estilos generales del body
   - Efectos de hover y transiciones

2. **`home.css`** - Estilos específicos para la página de inicio
   - Banner principal
   - Grid de productos
   - Estilos responsivos

3. **`noticias.css`** - Estilos específicos para la sección de noticias
   - Cards de noticias
   - Formularios
   - Botones específicos
   - Alertas

## Uso en templates

### Template base
- `core/templates/core/base.html` - Template base que incluye navegación y footer
- Carga automáticamente `base.css`
- Permite bloques `extra_css` para estilos específicos

### Templates específicos
Los templates ahora extienden del template base y solo cargan CSS específico:

```django
{% extends 'core/base.html' %}
{% load static %}

{% block extra_css %}
<link rel="stylesheet" href="{% static 'css/home.css' %}">
{% endblock %}
```

## Ventajas de esta estructura

1. **Mantenibilidad**: CSS separado del HTML
2. **Reutilización**: Estilos base compartidos
3. **Performance**: Cache de archivos CSS
4. **Organización**: Cada sección tiene su propio CSS
5. **Escalabilidad**: Fácil agregar nuevos estilos

## Configuración en Django

En `settings.py`:
```python
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'
```

## Estructura de directorios

```
FondaApp/
├── static/
│   ├── css/
│   │   ├── base.css
│   │   ├── home.css
│   │   └── noticias.css
│   ├── js/
│   └── images/
├── core/templates/core/
│   ├── base.html
│   └── home.html
└── noticias/templates/noticias/
    ├── base.html
    └── lista.html
```
