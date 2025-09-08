from django.contrib import admin
from django.urls import path
from core import views

urlpatterns = [
    path('sobrenosotros/', views.sobre_nosotros, name='sobrenosotros'),
    path('promociones/', views.promociones, name='promociones'),
    path('recetas/', views.recetas, name='recetas'),
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
]
