from django.urls import path
from . import views

<<<<<<< HEAD
app_name = 'tutor_ia'

urlpatterns = [
    path('', views.TutorIAView.as_view(), name='chat'),
    path('enviar-mensaje/', views.TutorIAView.as_view(), name='enviar_mensaje'),
=======
urlpatterns = [
    path('chat/', views.chat_tutor, name='chat_tutor'),
    path('api/mensaje/', views.api_mensaje_tutor, name='api_mensaje_tutor'),
>>>>>>> fee057efb0ba0c7861410146aa6286c538829f5a
]