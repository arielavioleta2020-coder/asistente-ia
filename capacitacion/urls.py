from django.urls import path
from . import views

urlpatterns = [
    path('modulos/', views.lista_modulos, name='lista_modulos'),
    path('modulo/<int:modulo_id>/', views.detalle_modulo, name='detalle_modulo'),
    path('leccion/<int:leccion_id>/', views.detalle_leccion, name='detalle_leccion'),
]