import requests
import json
import time

WEBHOOK_URL = "http://localhost:8765"

# Contexto del proyecto
CONTEXT = {
    "nombre": "Daniel Rojas",
    "rol": "Consultor de IA y Diseño para Pymes",
    "ubicacion": "Cali, Colombia",
    "whatsapp": "+57 317 444 6641",
    "servicios": ["landing pages", "chatbots", "automatizaciones", "diseño"],
    "mercado": "Cali primero, luego LATAM",
    "objetivo": "$2M COP/mes mínimo",
    "proyectos": {
        "decompas": "Landing page rediseñada con colores profesionales",
        "bot_discord": "Bot para recibir mensajes via !opencode",
        "webhook": "Servidor en puerto 8765 para comunicar OpenCode con Hermes",
        "opencode_web": "Servidor web en puerto 4096"
    },
    "portafolio": ["TIR", "E-Signer", "Silin", "Paycool", "Innu", "Linklight"]
}

def process_message(message):
    """Procesa un mensaje y genera una respuesta más inteligente"""
    message_lower = message.lower()
    
    # Detectar intención del mensaje
    if any(word in message_lower for word in ["hola", "buenos", "buenas"]):
        return "Hola! Soy OpenCode, tu consultor de IA y diseño. Estoy aquí para ayudarte con:\n- Landing pages y presencia digital\n- Automatización con IA\n- Chatbots y WhatsApp\n- Propuestas para clientes\n\n¿En qué puedo ayudarte?"
    
    elif any(word in message_lower for word in ["propuesta", "presupuesto", "cotización", "costo"]):
        if "restaurante" in message_lower:
            return "Para un restaurante puedo ayudarte con:\n\n1. Chatbot de WhatsApp para reservas y pedidos\n2. Página web con menú digital\n3. Sistema de pedidos online\n4. Automatización de confirmaciones\n\n¿Quieres que te prepare una propuesta? Dame el nombre del restaurante y tu WhatsApp."
        elif "clínica" in message_lower or "doctor" in message_lower:
            return "Para una clínica puedo ofrecerte:\n\n1. Chatbot para agendar citas\n2. Sistema de recordatorios por WhatsApp\n3. Historial digital de pacientes\n4. Página web con información de servicios\n\n¿Necesitas una propuesta específica?"
        elif "tienda" in message_lower or "ecommerce" in message_lower:
            return "Para una tienda online puedo ayudarte con:\n\n1. Chatbot de atención al cliente\n2. Automatización de pedidos\n3. Sistema de inventario\n4. Página web profesional\n\n¿Quieres que te prepare una cotización?"
        else:
            return "Puedo ayudarte con propuestas para:\n- Restaurantes: chatbots, reservas, pedidos\n- Clínicas: citas, recordatorios, historial\n- Tiendas: atención, pedidos, inventario\n- Servicios profesionales: consultoría, agendamiento\n\n¿Para qué tipo de negocio necesitas la propuesta?"
    
    elif any(word in message_lower for word in ["automatizar", "automatización", "proceso"]):
        if "whatsapp" in message_lower:
            return "La automatización de WhatsApp incluye:\n\n1. Respuestas automáticas a preguntas frecuentes\n2. Confirmación de pedidos/citas\n3. Seguimiento post-venta\n4. Notificaciones de estado\n\nEl costo depende del volumen. ¿Cuántos mensajes al día manejas?"
        elif "correo" in message_lower or "email" in message_lower:
            return "La automatización de correo incluye:\n\n1. Respuestas automáticas\n2. Secuencias de seguimiento\n3. Notificaciones\n4. Reportes automáticos\n\n¿Qué correo quieres automatizar?"
        else:
            return "Puedo automatizar:\n- WhatsApp: respuestas, pedidos, citas\n- Correo: seguimiento, notificaciones\n- Redes sociales: publicaciones, respuestas\n- CRM: actualización, reportes\n- Inventario: sincronización, alertas\n\n¿Qué proceso quieres automatizar?"
    
    elif any(word in message_lower for word in ["chatbot", "bot", "asistente"]):
        if "whatsapp" in message_lower:
            return "Un chatbot de WhatsApp puede:\n\n1. Responder preguntas frecuentes\n2. Hacer cotizaciones\n3. Agendar citas\n4. Tomar pedidos\n5. Calificar leads\n\n¿Quieres que te prepare una demo?"
        elif "web" in message_lower or "página" in message_lower:
            return "Un chatbot web puede:\n\n1. Atender visitantes 24/7\n2. Calificar leads\n3. Responder dudas\n4. Recopilar información\n5. Transferir a humano\n\n¿Lo quieres integrar con tu landing?"
        else:
            return "Los chatbots pueden ser para:\n- WhatsApp: atención y ventas\n- Web: soporte y calificación\n- Facebook/Instagram: respuestas automáticas\n- Telegram: información y pedidos\n\n¿Para qué plataforma lo necesitas?"
    
    elif any(word in message_lower for word in ["propuesta", "caso", "ejemplo"]):
        if "restaurante" in message_lower:
            return "Ejemplo de propuesta para restaurante:\n\n**Restaurante El Buen Sabor**\n\nProblema: Pierden pedidos por WhatsApp fuera de horario\n\nSolución:\n- Chatbot 24/7 para pedidos\n- Confirmación automática\n- Seguimiento post-pedid\n\nResultado: +30% pedidos, -50% tiempo de respuesta\n\n¿Quieres algo similar?"
        else:
            return "Puedo crear propuestas personalizadas para:\n- Restaurantes\n- Clínicas\n- Tiendas\n- Servicios profesionales\n\n¿Para qué negocio necesitas la propuesta?"
    
    elif any(word in message_lower for word in ["portafolio", "casos"]):
        return "Portafolio de proyectos:\n\n1. **TIR** - App móvil fintech\n2. **E-Signer** - Plataforma de firma electrónica\n3. **Silin** - Sistema de gestión de equipos\n4. **Paycool** - E-commerce de moda\n5. **Innu** - Plataforma educativa\n6. **Linklight** - Comparador financiero\n\n¿Quieres que te muestre detalles de alguno?"
    
    elif any(word in message_lower for word in ["decompas", "landing"]):
        return "Estado del proyecto Decompas:\n\n✅ Landing page rediseñada (colores profesionales)\n✅ Bot de Discord creado\n✅ Webhook server funcionando\n✅ Sistema de sincronización activo\n\nArchivos en: X:\\Proyectos IA OpenCode\\decompas\\\n\n¿Qué necesitas que haga ahora?"
    
    elif any(word in message_lower for word in ["precio", "costo", "cuánto", "cuanto"]):
        return "Mis servicios:\n\n- Landing page: $500,000 - $1,500,000 COP\n- Chatbot WhatsApp: $300,000 - $800,000 COP\n- Automatización: $500,000 - $2,000,000 COP\n- Propuesta completa: $200,000 - $500,000 COP\n\n¿Qué servicio te interesa?"
    
    elif any(word in message_lower for word in ["ayuda", "help", "opciones", "qué puedes"]):
        return "Puedo ayudarte con:\n\n1. **Propuestas** - Crear propuestas para clientes\n2. **Automatizar** - WhatsApp, correo, procesos\n3. **Chatbots** - Asistentes virtuales\n4. **Landing** - Páginas web profesionales\n5. **Portafolio** - Ver proyectos anteriores\n\n¿Qué necesitas?"
    
    elif any(word in message_lower for word in ["gracias"]):
        return "¡De nada! Estoy aquí para lo que necesites. ¿Hay algo más en que pueda ayudarte?"
    
    elif any(word in message_lower for word in ["adiós", "adios", "chao", "bye"]):
        return "¡Hasta luego! Estaré aquí cuando me necesites. ¡Éxitos con tu negocio!"
    
    else:
        return f"Entiendo que necesitas ayuda con: '{message}'. Puedo ayudarte con propuestas, automatización, chatbots y más. ¿Qué necesitas específicamente?"

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