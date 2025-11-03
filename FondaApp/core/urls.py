from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('sobrenosotros/', views.sobre_nosotros, name='sobrenosotros'),
    path('promociones/', views.promociones, name='promociones'),
    path('recetas/', views.recetas, name='recetas'),
]
