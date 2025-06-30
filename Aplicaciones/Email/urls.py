from django.urls import path
from . import views

urlpatterns = [
    path('listarMensajes', views.inicio, name='listarMensajes'),
    path('nuevoMensaje', views.nuevoMensaje, name='nuevo_mensaje'),
    path('guardarMensaje', views.guardarMensaje, name='guardar_mensaje'),
    path('eliminarMensaje<int:id>', views.eliminarMensaje, name='eliminar_mensaje'),
    path('editarMensaje<int:id>', views.editarMensaje, name='editar_mensaje'),
    path('procesarEdicionMensaje', views.procesarEdicionMensaje, name='procesar_edicion'),
    path('enviarMensaje<int:id>', views.enviarMensaje, name='enviar_mensaje'),
]