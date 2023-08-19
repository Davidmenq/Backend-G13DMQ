#aqui declararemos todas las rutas pertenecientes a esta aplicacion

from django.urls import path
from .views import paginaInicio, DevolverHoraServidor, CategirasController, CategoriaController # cuando se coloca . se incica un archivo en el mismo nivel

urlpatterns = [
    path('inicio', paginaInicio),
    path('status', DevolverHoraServidor),
    path('categorias', CategirasController.as_view()),
    path('categoria/<id>', CategoriaController.as_view())
  
]