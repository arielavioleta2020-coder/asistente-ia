from django.urls import path
from . import views

<<<<<<< HEAD
app_name = 'usuarios'

=======
>>>>>>> fee057efb0ba0c7861410146aa6286c538829f5a
urlpatterns = [
    path('dashboard/', views.dashboard_usuario, name='dashboard_usuario'),
    path('perfil/', views.perfil_usuario, name='perfil_usuario'),
    path('editar-perfil/', views.editar_perfil, name='editar_perfil'),
]