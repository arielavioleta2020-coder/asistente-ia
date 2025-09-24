from django.db import models
from capacitacion.models import Modulo

class PreguntaFrecuente(models.Model):
    modulo = models.ForeignKey(Modulo, on_delete=models.CASCADE)
    pregunta = models.TextField()
    respuesta = models.TextField()
    palabras_clave = models.TextField(help_text="Palabras clave separadas por coma")
    
    def __str__(self):
        return self.pregunta[:50] + "..."