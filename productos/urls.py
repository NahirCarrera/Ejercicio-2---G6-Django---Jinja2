from django.urls import path
from . import views

urlpatterns = [
    # URLs de vistas normales
    path('', views.listar_productos, name='listar_productos'),
    path('exportar_csv/', views.exportar_csv, name='exportar_csv'),
    path('importar_csv/', views.importar_csv, name='importar_csv'),
    path('productos/crear/', views.crear_producto, name='crear_producto'),
    path('productos/editar/<int:pk>/', views.editar_producto, name='editar_producto'),
    path('productos/eliminar/<int:pk>/', views.eliminar_producto, name='eliminar_producto'),
]