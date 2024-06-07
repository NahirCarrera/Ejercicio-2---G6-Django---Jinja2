from django.urls import path
from . import views

urlpatterns = [
    # URLs de vistas normales
    path('', views.listar_productos, name='listar_productos'),
    path('exportar_csv/', views.exportar_csv, name='exportar_csv'),
    path('importar_csv/', views.importar_csv, name='importar_csv'),
    
]