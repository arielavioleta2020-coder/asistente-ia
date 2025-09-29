from django.urls import path
from . import views

urlpatterns = [
    path('iniciar/', views.iniciar_diagnostico, name='iniciar_diagnostico'),
    path('resultado/', views.resultado_diagnostico, name='resultado_diagnostico'),
    path('dashboard/', views.dashboard_diagnostico, name='dashboard_diagnostico'),
]
