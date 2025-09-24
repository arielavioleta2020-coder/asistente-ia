from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json

# Base de conocimiento simple para el tutor IA
BASE_CONOCIMIENTO = {
    'seguridad': {
        'preguntas': [
            "¿Qué es el phishing?",
            "¿Cómo crear una contraseña segura?",
            "¿Qué es un antivirus?"
        ],
        'respuestas': [
            "El phishing es un intento de obtener información confidencial haciéndose pasar por una comunicación confiable.",
            "Una contraseña segura debe tener al menos 8 caracteres, incluir mayúsculas, minúsculas, números y símbolos.",
            "Un antivirus es un software que detecta y elimina malware y virus informáticos."
        ]
    },
    'ofimatica': {
        'preguntas': [
            "¿Qué es Excel?",
            "¿Cómo formatear texto en Word?",
            "¿Qué es PowerPoint?"
        ],
        'respuestas': [
            "Excel es una hoja de cálculo para organizar y analizar datos.",
            "En Word, selecciona el texto y usa las opciones de la pestaña 'Inicio' para formatear.",
            "PowerPoint es un programa para crear presentaciones visuales."
        ]
    }
}

@login_required
def chat_tutor(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            pregunta = data.get('pregunta', '').lower()
            
            # Búsqueda simple por palabras clave
            respuesta = "Lo siento, no tengo información sobre ese tema. ¿Podrías reformular la pregunta?"
            
            for tema, contenido in BASE_CONOCIMIENTO.items():
                if tema in pregunta:
                    # Buscar pregunta similar
                    for i, preg in enumerate(contenido['preguntas']):
                        if any(palabra in pregunta for palabra in preg.lower().split()):
                            respuesta = contenido['respuestas'][i]
                            break
                    else:
                        respuesta = f"Para el tema de {tema}, puedo ayudarte con: {', '.join(contenido['preguntas'])}"
                    break
                elif 'hola' in pregunta or 'ayuda' in pregunta:
                    respuesta = "¡Hola! Soy tu tutor IA. Puedo ayudarte con temas de seguridad digital y ofimática. ¿En qué necesitas ayuda?"
            
            return JsonResponse({'respuesta': respuesta})
        
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Formato JSON inválido'}, status=400)
    
    return render(request, 'tutor_ia/chat.html')