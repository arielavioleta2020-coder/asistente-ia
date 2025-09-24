from django.contrib import admin
from .models import PreguntaFrecuente

@admin.register(PreguntaFrecuente)
class PreguntaFrecuenteAdmin(admin.ModelAdmin):
    list_display = ['pregunta', 'modulo']
    list_filter = ['modulo']