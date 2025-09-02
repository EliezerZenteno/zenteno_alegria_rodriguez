from django.contrib import admin
from django.urls import path
from core import views

urlpatterns = [
    path('historia/', views.historia, name='historia'),
    path('sobre_nosotros/', views.sobre_nosotros, name='sobre_nosotros'),
    path('promociones/', views.promociones, name='promociones'),
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
]
