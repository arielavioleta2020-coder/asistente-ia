from django.shortcuts import render
<<<<<<< HEAD
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views import View
import json

class TutorIAView(View):
    def get(self, request):
        return render(request, 'tutor_ia/chat.html')
    
    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    def post(self, request):
        try:
            data = json.loads(request.body)
            mensaje = data.get('mensaje', '').strip().lower()
            
            if not mensaje:
                return JsonResponse({'success': False, 'error': 'Mensaje vacío'})
            
            # Respuestas predeterminadas basadas en palabras clave
            respuesta = self.obtener_respuesta(mensaje)
            
            return JsonResponse({
                'success': True, 
                'respuesta': respuesta
            })
            
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    def obtener_respuesta(self, mensaje):
        # Diccionario de preguntas frecuentes y respuestas
        faqs = {
            # Diagnóstico
            'diagnóstico': "🔍 **Sistema de Diagnóstico**\n\nEl diagnóstico evalúa tus conocimientos en Python, Django, HTML, CSS y JavaScript. Consiste en preguntas de múltiple opción que te ayudarán a identificar tu nivel actual.",
            'diagnostico': "🔍 **Sistema de Diagnóstico**\n\nEl diagnóstico evalúa tus conocimientos en Python, Django, HTML, CSS y JavaScript. Consiste en preguntas de múltiple opción que te ayudarán a identificar tu nivel actual.",
            'evaluación': "🔍 **Sistema de Diagnóstico**\n\nEl diagnóstico evalúa tus conocimientos en Python, Django, HTML, CSS y JavaScript. Consiste en preguntas de múltiple opción que te ayudarán a identificar tu nivel actual.",
            'test': "🔍 **Sistema de Diagnóstico**\n\nEl diagnóstico evalúa tus conocimientos en Python, Django, HTML, CSS y JavaScript. Consiste en preguntas de múltiple opción que te ayudarán a identificar tu nivel actual.",
            
            # Python
            'python': "🐍 **Python**\n\nPython es un lenguaje de programación fácil de aprender, ideal para principiantes. Se usa para desarrollo web, análisis de datos, inteligencia artificial y más.",
            'qué es python': "🐍 **Python**\n\nPython es un lenguaje de programación interpretado de alto nivel. Su sintaxis clara lo hace perfecto para empezar en programación.",
            'que es python': "🐍 **Python**\n\nPython es un lenguaje de programación interpretado de alto nivel. Su sintaxis clara lo hace perfecto para empezar en programación.",
            
            # Django
            'django': "🎸 **Django**\n\nDjango es un framework web de Python que facilita la creación de aplicaciones web robustas y seguras. Incluye ORM, panel de administración y autenticación.",
            'qué es django': "🎸 **Django**\n\nDjango es un framework web que sigue el patrón MVT (Modelo-Vista-Template). Es ideal para desarrollar aplicaciones web complejas rápidamente.",
            'que es django': "🎸 **Django**\n\nDjango es un framework web que sigue el patrón MVT (Modelo-Vista-Template). Es ideal para desarrollar aplicaciones web complejas rápidamente.",
            
            # Frontend
            'html': "🌐 **HTML**\n\nHTML es el lenguaje estándar para crear páginas web. Define la estructura y el contenido usando etiquetas como <h1>, <p>, <div>.",
            'css': "🎨 **CSS**\n\nCSS se usa para dar estilo a las páginas web. Controla colores, fuentes, diseños y la apariencia general del sitio.",
            'javascript': "⚡ **JavaScript**\n\nJavaScript hace que las páginas web sean interactivas. Se ejecuta en el navegador y permite crear efectos, validar formularios y más.",
            
            # Plataforma
            'plataforma': "🖥️ **Plataforma**\n\nNuestra plataforma ofrece diagnóstico inicial, contenido personalizado y seguimiento de progreso. Comienza con el diagnóstico para obtener recomendaciones.",
            'cómo usar': "🖥️ **Uso de la Plataforma**\n\n1. Realiza el diagnóstico inicial\n2. Revisa tus resultados\n3. Accede al contenido recomendado\n4. Practica con ejercicios",
            'como usar': "🖥️ **Uso de la Plataforma**\n\n1. Realiza el diagnóstico inicial\n2. Revisa tus resultados\n3. Accede al contenido recomendado\n4. Practica con ejercicios",
            
            # Ayuda general
            'ayuda': "🤖 **Asistente Virtual**\n\nPuedo ayudarte con:\n• Información sobre el diagnóstico\n• Explicaciones de Python, Django\n• Conceptos de HTML, CSS, JavaScript\n• Uso de la plataforma\n\nUsa los botones de preguntas rápidas o escribe tu duda.",
            'help': "🤖 **Asistente Virtual**\n\nPuedo ayudarte con:\n• Información sobre el diagnóstico\n• Explicaciones de Python, Django\n• Conceptos de HTML, CSS, JavaScript\n• Uso de la plataforma\n\nUsa los botones de preguntas rápidas o escribe tu duda.",
        }
        
        # Buscar coincidencias exactas primero
        if mensaje in faqs:
            return faqs[mensaje]
        
        # Buscar palabras clave en el mensaje
        for palabra_clave, respuesta in faqs.items():
            if palabra_clave in mensaje:
                return respuesta
        
        # Respuesta por defecto si no encuentra coincidencia
        return "❓ **Pregunta no reconocida**\n\nNo encuentro una respuesta para tu pregunta. Puedo ayudarte con:\n\n• **Diagnóstico del sistema**\n• **Python y Django**\n• **HTML, CSS, JavaScript**\n• **Uso de la plataforma**\n\nUsa los botones de preguntas rápidas o intenta con términos más específicos."
=======
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
>>>>>>> fee057efb0ba0c7861410146aa6286c538829f5a
