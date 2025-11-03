from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('sobrenosotros/', views.sobre_nosotros, name='sobrenosotros'),
    path('promociones/', views.promociones, name='promociones'),
    path('recetas/', views.recetas, name='recetas'),
    path('noticias/', include('noticias.urls')),
    path('contacto/', include('contacto.urls')),
]

# Handler para error 404 personalizado
handler404 = 'core.views.error_404'

# Servir archivos media en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
