from django.db import models
from django.contrib.auth.models import User

class PreguntaFrecuente(models.Model):
    pregunta = models.CharField(max_length=255)
    respuesta = models.TextField()
    categoria = models.CharField(max_length=100, default="General")
    activa = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.pregunta
    
    class Meta:
        verbose_name = "Pregunta Frecuente"
        verbose_name_plural = "Preguntas Frecuentes"

class Conversacion(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=200, default="Conversación")
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.username} - {self.titulo}"

class Mensaje(models.Model):
    conversacion = models.ForeignKey(Conversacion, on_delete=models.CASCADE, related_name='mensajes')
    contenido = models.TextField()
    es_usuario = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{'Usuario' if self.es_usuario else 'IA'}: {self.contenido[:50]}..."

from capacitacion.models import Modulo

class PreguntaFrecuente(models.Model):
    modulo = models.ForeignKey(Modulo, on_delete=models.CASCADE)
    pregunta = models.TextField()
    respuesta = models.TextField()
    palabras_clave = models.TextField(help_text="Palabras clave separadas por coma")
    
    def __str__(self):
        return self.pregunta[:50] + "..."

