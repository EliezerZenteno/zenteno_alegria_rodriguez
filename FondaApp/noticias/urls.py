from django.urls import path
from . import views

app_name = 'noticias'

urlpatterns = [
    path('', views.lista_noticias, name='lista'),
    path('<int:pk>/', views.detalle_noticia, name='detalle'),
    path('<int:pk>/comentario/', views.crear_comentario, name='crear_comentario'),
    # Las siguientes rutas están deshabilitadas para uso público
    # Solo se pueden gestionar noticias desde el admin de Django
    # path('crear/', views.crear_noticia, name='crear'),
    # path('<int:pk>/editar/', views.editar_noticia, name='editar'),
    # path('<int:pk>/eliminar/', views.eliminar_noticia, name='eliminar'),
]
