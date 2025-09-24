from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, Http404
from django.contrib import messages
from django.db import transaction
from django.utils import timezone
from .models import Modulo, Pregunta, DiagnosticoUsuario, RespuestaUsuario, OpcionRespuesta
from .forms import DiagnosticoForm
import json

@login_required
@transaction.atomic
def iniciar_diagnostico(request):
    """
    Vista para iniciar el diagnóstico del usuario.
    Si ya tiene uno en progreso, lo continúa. Si no, crea uno nuevo.
    """
    try:
        # Buscar diagnóstico existente no completado
        diagnostico = DiagnosticoUsuario.objects.filter(
            usuario=request.user,
            completado=False
        ).first()
        
        # Si no existe, crear uno nuevo
        if not diagnostico:
            diagnostico = DiagnosticoUsuario.objects.create(
                usuario=request.user,
                completado=False,
                fecha_inicio=timezone.now()
            )
        
        # Obtener todas las preguntas ordenadas
        preguntas = Pregunta.objects.all().order_by('modulo__id', 'orden')
        
        if not preguntas.exists():
            messages.warning(request, "No hay preguntas disponibles para el diagnóstico.")
            return redirect('dashboard_usuario')
        
        if request.method == 'POST':
            # Procesar respuestas del formulario
            for key, value in request.POST.items():
                if key.startswith('pregunta_'):
                    try:
                        pregunta_id = key.replace('pregunta_', '')
                        pregunta = get_object_or_404(Pregunta, id=pregunta_id)
                        opcion_seleccionada = get_object_or_404(OpcionRespuesta, id=value)
                        
                        # Guardar o actualizar respuesta
                        respuesta, created = RespuestaUsuario.objects.get_or_create(
                            diagnostico=diagnostico,
                            pregunta=pregunta
                        )
                        respuesta.opcion_seleccionada = opcion_seleccionada
                        respuesta.fecha_respuesta = timezone.now()
                        respuesta.save()
                        
                    except (Pregunta.DoesNotExist, OpcionRespuesta.DoesNotExist):
                        messages.error(request, f"Error al procesar la pregunta {pregunta_id}")
                        continue
            
            # Marcar diagnóstico como completado
            diagnostico.completado = True
            diagnostico.fecha_finalizacion = timezone.now()
            diagnostico.save()
            
            messages.success(request, "¡Diagnóstico completado exitosamente!")
            return redirect('resultado_diagnostico')
        
        # Obtener respuestas previas para pre-seleccionar opciones
        respuestas_previas = RespuestaUsuario.objects.filter(
            diagnostico=diagnostico
        ).select_related('opcion_seleccionada')
        
        # Crear formulario con datos iniciales si existen respuestas previas
        initial_data = {}
        for respuesta in respuestas_previas:
            initial_data[f'pregunta_{respuesta.pregunta.id}'] = respuesta.opcion_seleccionada.id
        
        form = DiagnosticoForm(preguntas=preguntas, initial=initial_data)
        
        return render(request, 'diagnostico/cuestionario.html', {
            'form': form,
            'preguntas': preguntas,
            'diagnostico': diagnostico,
            'total_preguntas': preguntas.count(),
            'preguntas_respondidas': respuestas_previas.count()
        })
    
    except Exception as e:
        messages.error(request, f"Error al iniciar el diagnóstico: {str(e)}")
        return redirect('dashboard_usuario')

@login_required
def resultado_diagnostico(request):
    """
    Vista para mostrar los resultados del diagnóstico completado
    """
    try:
        # Obtener el último diagnóstico completado
        diagnostico = DiagnosticoUsuario.objects.filter(
            usuario=request.user,
            completado=True
        ).order_by('-fecha_finalizacion').first()
        
        if not diagnostico:
            messages.warning(request, "No has completado ningún diagnóstico aún.")
            return redirect('iniciar_diagnostico')
        
        # Obtener todas las respuestas del diagnóstico
        respuestas = RespuestaUsuario.objects.filter(
            diagnostico=diagnostico
        ).select_related('pregunta', 'pregunta__modulo', 'opcion_seleccionada')
        
        if not respuestas.exists():
            messages.warning(request, "No se encontraron respuestas para este diagnóstico.")
            return redirect('iniciar_diagnostico')
        
        # Calcular resultados por módulo
        resultados_por_modulo = {}
        for respuesta in respuestas:
            modulo = respuesta.pregunta.modulo
            modulo_nombre = modulo.nombre
            
            if modulo_nombre not in resultados_por_modulo:
                resultados_por_modulo[modulo_nombre] = {
                    'modulo': modulo,
                    'puntuacion_total': 0,
                    'preguntas_respondidas': 0,
                    'puntuacion_maxima': 0,
                    'respuestas': []
                }
            
            resultado_modulo = resultados_por_modulo[modulo_nombre]
            resultado_modulo['puntuacion_total'] += respuesta.opcion_seleccionada.valor
            resultado_modulo['preguntas_respondidas'] += 1
            resultado_modulo['puntuacion_maxima'] += 5  # Máximo 5 por pregunta
            resultado_modulo['respuestas'].append(respuesta)
        
        # Calcular porcentajes y determinar nivel de competencia
        for modulo_nombre, datos in resultados_por_modulo.items():
            if datos['puntuacion_maxima'] > 0:
                datos['porcentaje'] = (datos['puntuacion_total'] / datos['puntuacion_maxima']) * 100
                
                # Determinar nivel de competencia basado en el porcentaje
                if datos['porcentaje'] >= 80:
                    datos['nivel'] = 'Avanzado'
                    datos['color'] = 'success'
                elif datos['porcentaje'] >= 60:
                    datos['nivel'] = 'Intermedio'
                    datos['color'] = 'info'
                elif datos['porcentaje'] >= 40:
                    datos['nivel'] = 'Básico'
                    datos['color'] = 'warning'
                else:
                    datos['nivel'] = 'Principiante'
                    datos['color'] = 'danger'
            else:
                datos['porcentaje'] = 0
                datos['nivel'] = 'Sin datos'
                datos['color'] = 'secondary'
        
        # Calcular resultados generales
        puntuacion_total_general = sum(datos['puntuacion_total'] for datos in resultados_por_modulo.values())
        puntuacion_maxima_general = sum(datos['puntuacion_maxima'] for datos in resultados_por_modulo.values())
        porcentaje_general = (puntuacion_total_general / puntuacion_maxima_general * 100) if puntuacion_maxima_general > 0 else 0
        
        return render(request, 'diagnostico/resultado.html', {
            'resultados': resultados_por_modulo,
            'diagnostico': diagnostico,
            'total_preguntas': respuestas.count(),
            'puntuacion_total_general': puntuacion_total_general,
            'puntuacion_maxima_general': puntuacion_maxima_general,
            'porcentaje_general': porcentaje_general,
            'modulos_evaluados': len(resultados_por_modulo)
        })
    
    except Exception as e:
        messages.error(request, f"Error al cargar los resultados: {str(e)}")
        return redirect('dashboard_usuario')

@login_required
def dashboard_diagnostico(request):
    """
    Dashboard principal del diagnóstico que muestra el progreso del usuario
    """
    try:
        # Obtener diagnóstico activo (no completado)
        diagnostico_activo = DiagnosticoUsuario.objects.filter(
            usuario=request.user,
            completado=False
        ).first()
        
        # Obtener últimos diagnósticos completados
        diagnosticos_completados = DiagnosticoUsuario.objects.filter(
            usuario=request.user,
            completado=True
        ).order_by('-fecha_finalizacion')[:5]  # Últimos 5 diagnósticos
        
        # Obtener estadísticas generales
        total_diagnosticos = DiagnosticoUsuario.objects.filter(usuario=request.user).count()
        diagnosticos_completados_count = DiagnosticoUsuario.objects.filter(
            usuario=request.user, 
            completado=True
        ).count()
        
        # Si hay un diagnóstico completado reciente, mostrar sus resultados resumidos
        ultimo_diagnostico = diagnosticos_completados.first()
        resultados_resumidos = None
        
        if ultimo_diagnostico:
            respuestas = RespuestaUsuario.objects.filter(
                diagnostico=ultimo_diagnostico
            ).select_related('pregunta__modulo', 'opcion_seleccionada')
            
            # Calcular resumen rápido
            modulos_evaluados = set()
            puntuacion_total = 0
            puntuacion_maxima = 0
            
            for respuesta in respuestas:
                modulos_evaluados.add(respuesta.pregunta.modulo.nombre)
                puntuacion_total += respuesta.opcion_seleccionada.valor
                puntuacion_maxima += 5
            
            porcentaje_promedio = (puntuacion_total / puntuacion_maxima * 100) if puntuacion_maxima > 0 else 0
            
            resultados_resumidos = {
                'modulos_evaluados': len(modulos_evaluados),
                'puntuacion_total': puntuacion_total,
                'puntuacion_maxima': puntuacion_maxima,
                'porcentaje_promedio': porcentaje_promedio,
                'fecha': ultimo_diagnostico.fecha_finalizacion
            }
        
        return render(request, 'diagnostico/dashboard.html', {
            'diagnostico_activo': diagnostico_activo,
            'diagnosticos_completados': diagnosticos_completados,
            'ultimo_diagnostico': ultimo_diagnostico,
            'resultados_resumidos': resultados_resumidos,
            'total_diagnosticos': total_diagnosticos,
            'diagnosticos_completados_count': diagnosticos_completados_count,
            'porcentaje_completados': (diagnosticos_completados_count / total_diagnosticos * 100) if total_diagnosticos > 0 else 0
        })
    
    except Exception as e:
        messages.error(request, f"Error al cargar el dashboard: {str(e)}")
        return render(request, 'diagnostico/dashboard.html', {
            'diagnostico_activo': None,
            'diagnosticos_completados': [],
            'error': str(e)
        })

@login_required
def reiniciar_diagnostico(request):
    """
    Vista para reiniciar el diagnóstico actual
    """
    try:
        # Eliminar diagnóstico actual no completado
        DiagnosticoUsuario.objects.filter(
            usuario=request.user,
            completado=False
        ).delete()
        
        # Eliminar respuestas asociadas
        diagnostico_completado = DiagnosticoUsuario.objects.filter(
            usuario=request.user,
            completado=True
        ).first()
        
        if diagnostico_completado:
            RespuestaUsuario.objects.filter(diagnostico=diagnostico_completado).delete()
        
        messages.info(request, "Diagnóstico reiniciado. Puedes comenzar de nuevo.")
        return redirect('iniciar_diagnostico')
    
    except Exception as e:
        messages.error(request, f"Error al reiniciar el diagnóstico: {str(e)}")
        return redirect('dashboard_diagnostico')

@login_required
def ver_progreso(request, diagnostico_id):
    """
    Vista para ver el progreso de un diagnóstico específico
    """
    try:
        diagnostico = get_object_or_404(
            DiagnosticoUsuario, 
            id=diagnostico_id, 
            usuario=request.user
        )
        
        if diagnostico.completado:
            return redirect('resultado_diagnostico')
        
        # Lógica similar a iniciar_diagnostico pero para continuar
        preguntas = Pregunta.objects.all().order_by('modulo__id', 'orden')
        respuestas_previas = RespuestaUsuario.objects.filter(
            diagnostico=diagnostico
        ).select_related('opcion_seleccionada')
        
        initial_data = {}
        for respuesta in respuestas_previas:
            initial_data[f'pregunta_{respuesta.pregunta.id}'] = respuesta.opcion_seleccionada.id
        
        form = DiagnosticoForm(preguntas=preguntas, initial=initial_data)
        
        return render(request, 'diagnostico/continuar.html', {
            'form': form,
            'preguntas': preguntas,
            'diagnostico': diagnostico,
            'total_preguntas': preguntas.count(),
            'preguntas_respondidas': respuestas_previas.count()
        })
    
    except Http404:
        messages.error(request, "Diagnóstico no encontrado.")
        return redirect('dashboard_diagnostico')

# Create your views here.
