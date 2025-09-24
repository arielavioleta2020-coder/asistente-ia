from django.urls import path
from . import views

urlpatterns = [
    path('chat/', views.chat_tutor, name='chat_tutor'),
    path('api/mensaje/', views.api_mensaje_tutor, name='api_mensaje_tutor'),
]