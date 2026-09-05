import requests
import json
import time
import sys
import io

# Configurar codificación
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

WEBHOOK_URL = "http://localhost:8765"

# Importar módulo de vector DB
sys.path.insert(0, r'X:\Proyectos IA OpenCode\Decompas')
from query_vectordb import obtener_contexto_para_respuesta

def process_message(message):
    """Procesa un mensaje usando contexto de la base de datos vectorial"""
    
    # Obtener contexto relevante de la base de datos vectorial
    contexto_vectorial = obtener_contexto_para_respuesta(message)
    
    # Detectar intención del mensaje
    message_lower = message.lower()
    
    # Saludos
    if any(word in message_lower for word in ["hola", "buenos", "buenas"]):
        return f"Hola! Soy OpenCode, el asistente de Daniel Rojas.\n\n{contexto_vectorial}\n¿En qué puedo ayudarte?"
    
    # Propuestas
    elif any(word in message_lower for word in ["propuesta", "presupuesto", "cotización", "costo"]):
        return f"Para crear una propuesta necesito:\n\n1. Nombre del negocio\n2. Tipo de negocio (restaurante, clínica, tienda, etc.)\n3. Problema que enfrentan\n4. WhatsApp de contacto\n\n{contexto_vectorial}\n\nDame esos datos y preparo la propuesta."
    
    # Automatización
    elif any(word in message_lower for word in ["automatizar", "automatización", "proceso"]):
        return f"La automatización puede incluir:\n\n- WhatsApp: respuestas automáticas, pedidos, citas\n- Correo: seguimiento, notificaciones\n- Redes sociales: publicaciones, respuestas\n- CRM: actualización, reportes\n\n{contexto_vectorial}\n\n¿Qué proceso quieres automatizar?"
    
    # Chatbots
    elif any(word in message_lower for word in ["chatbot", "bot", "asistente"]):
        return f"Los chatbots pueden ser para:\n\n- WhatsApp: atención y ventas 24/7\n- Web: soporte y calificación de leads\n- Facebook/Instagram: respuestas automáticas\n\n{contexto_vectorial}\n\n¿Para qué plataforma lo necesitas?"
    
    # Portafolio
    elif any(word in message_lower for word in ["portafolio", "proyectos", "casos"]):
        return f"Portafolio de Daniel:\n\n1. TIR - App móvil fintech\n2. E-Signer - Firma electrónica\n3. Silin - Gestión de equipos\n4. Paycool - E-commerce de moda\n5. Innu - Plataforma educativa\n6. Linklight - Comparador financiero\n\n{contexto_vectorial}\n\n¿Quieres detalles de alguno?"
    
    # Decompas
    elif any(word in message_lower for word in ["decompas", "landing"]):
        return f"Estado del proyecto Decompas:\n\n✅ Landing rediseñada con colores profesionales\n✅ Bot de Discord funcionando\n✅ Webhook server activo\n✅ OpenCode Web corriendo\n\n{contexto_vectorial}\n\n¿Qué necesitas?"
    
    # Precios
    elif any(word in message_lower for word in ["precio", "costo", "cuánto", "cuanto"]):
        return f"Rangos de precios:\n\n- Landing page: $500,000 - $1,500,000 COP\n- Chatbot WhatsApp: $300,000 - $800,000 COP\n- Automatización: $500,000 - $2,000,000 COP\n- Propuesta: $200,000 - $500,000 COP\n\n{contexto_vectorial}\n\n¿Qué servicio te interesa?"
    
    # Ayuda
    elif any(word in message_lower for word in ["ayuda", "help", "opciones", "qué puedes"]):
        return f"Puedo ayudarte con:\n\n1. Propuestas para clientes\n2. Automatización de procesos\n3. Chatbots y WhatsApp\n4. Landing pages\n5. Información del portafolio\n\n{contexto_vectorial}\n\n¿Qué necesitas?"
    
    # Gracias
    elif any(word in message_lower for word in ["gracias"]):
        return f"¡De nada! Estoy aquí para lo que necesites.\n\n{contexto_vectorial}"
    
    # Adiós
    elif any(word in message_lower for word in ["adiós", "adios", "chao", "bye"]):
        return "¡Hasta luego! Estaré aquí cuando me necesites."
    
    # Respuesta por defecto con contexto
    else:
        return f"Recibí tu mensaje: '{message}'\n\n{contexto_vectorial}\n\n¿Qué necesitas específicamente?"

def listen():
    print("Escuchando mensajes...")
    
    while True:
        try:
            response = requests.get(WEBHOOK_URL)
            data = response.json()
            messages = data.get("messages", [])
            
            for msg in messages:
                if msg["source"] == "hermes" and not msg.get("processed"):
                    print(f"[Hermes]: {msg['message']}")
                    
                    # Procesar mensaje
                    respuesta = process_message(msg["message"])
                    print(f"[OpenCode]: {respuesta[:100]}...")
                    
                    # Enviar respuesta
                    requests.post(WEBHOOK_URL, json={
                        "source": "opencode",
                        "message": respuesta
                    })
                    
                    # Marcar como procesado
                    requests.delete(WEBHOOK_URL, json={"id": msg["id"]})
                    
        except Exception as e:
            print(f"Error: {e}")
        
        time.sleep(3)

if __name__ == "__main__":
    listen()