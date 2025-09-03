from django.urls import path
from .views import productos_view, producto_id, agregar_producto

urlpatterns = [
    path('productos/', productos_view, name='productos_view'),
    path('productos/<int:pk>/', producto_id, name='producto_id'),
    path('productos/agregar/', agregar_producto, name='agregar_producto'),
]