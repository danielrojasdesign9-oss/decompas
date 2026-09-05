import chromadb
from chromadb.utils import embedding_functions
import json
from pathlib import Path

# Ruta de la base de datos
DB_PATH = Path("X:/Proyectos IA OpenCode/Decompas/vector_db")

# Crear cliente de ChromaDB
client = chromadb.PersistentClient(path=str(DB_PATH))

# Usar embedding function local (no necesita API)
ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")

# Crear o obtener colección
collection = client.get_or_create_collection(
    name="decompas_context",
    embedding_function=ef
)

# Contexto completo del proyecto de mentoria
contextos = [
    # Información personal
    {
        "id": "daniel_1",
        "texto": "Daniel Rojas es un consultor de IA y Diseño para Pymes ubicado en Cali, Colombia. Su WhatsApp es +57 317 444 6641. Se especializa en automatización de negocios pequeños y medianos.",
        "categoria": "personal"
    },
    {
        "id": "daniel_2",
        "texto": "Daniel ofrece servicios de: landing pages profesionales, chatbots de WhatsApp, automatización de procesos, diseño de interfaces, sistemas de diseño, y consultoría de IA para empresas.",
        "categoria": "servicios"
    },
    {
        "id": "daniel_3",
        "texto": "El mercado objetivo de Daniel es Cali primero, luego expandirse a Latinoamérica (LATAM). Su objetivo de ingresos es mínimo $2,000,000 COP por mes.",
        "categoria": "negocio"
    },
    
    # Proyecto Decompas
    {
        "id": "decompas_1",
        "texto": "Decompas es la landing page de Daniel. URL: https://decompas.netlify.app. Repositorio: https://github.com/danielrojasdesign9-oss/decompas. Los archivos están en X:\\Proyectos IA OpenCode\\Decompas\\",
        "categoria": "proyecto"
    },
    {
        "id": "decompas_2",
        "texto": "La landing de Decompas fue rediseñada con colores profesionales: azul oscuro #1a2332 y gris claro #f8f6f3. Se eliminó la calculadora de conversión, las estadísticas AI, y el copy se reescribió sin bullets, números ni flechas.",
        "categoria": "proyecto"
    },
    {
        "id": "decompas_3",
        "texto": "La landing de Decompas incluye: sección de servicios (agentes IA, automatización, diseño), casos de estudio del portafolio (TIR, E-Signer, Silin, Paycool, Innu, Linklight), proceso de trabajo, formulario de contacto.",
        "categoria": "proyecto"
    },
    
    # Portafolio
    {
        "id": "portafolio_1",
        "texto": "Portafolio de Daniel: 1) TIR - App móvil fintech, 2) E-Signer - Plataforma de firma electrónica, 3) Silin - Sistema de gestión de equipos, 4) Paycool - E-commerce de moda, 5) Innu - Plataforma educativa, 6) Linklight - Comparador financiero.",
        "categoria": "portafolio"
    },
    {
        "id": "portafolio_2",
        "texto": "Los proyectos del portafolio son casos de uso reales que Daniel puede mostrar a clientes potenciales para demostrar su experiencia en diseño y desarrollo de productos digitales.",
        "categoria": "portafolio"
    },
    
    # Bot de Discord
    {
        "id": "bot_1",
        "texto": "El bot de Discord de Daniel usa el comando !opencode para enviar mensajes a OpenCode. El bot está configurado en opencode_bot_v3.py y usa el webhook en localhost:8765.",
        "categoria": "tecnico"
    },
    {
        "id": "bot_2",
        "texto": "Flujo del bot: Usuario escribe !opencode [mensaje] → Bot envía al webhook → Listener procesa → OpenCode responde → Bot muestra respuesta en Discord.",
        "categoria": "tecnico"
    },
    
    # OpenCode Web
    {
        "id": "opencode_1",
        "texto": "OpenCode Web Server está corriendo en http://desktop-ide6st8:4096. Usuario: danielremoto, Contraseña: makiMa12*. Se accede desde el celular via Tailscale.",
        "categoria": "tecnico"
    },
    
    # Tailscale
    {
        "id": "tailscale_1",
        "texto": "Daniel usa Tailscale para acceder a su PC desde el celular. IP de la PC: 100.90.233.116, Nombre: desktop-ide6st8. El celular es Nothing Phone 3a Pro.",
        "categoria": "tecnico"
    },
    
    # Ejercicios
    {
        "id": "ejercicios_1",
        "texto": "Ejercicios para usar Hermes + OpenCode: 1) Investigar negocios en Cali, 2) Crear propuestas personalizadas, 3) Auditar presencia digital, 4) Crear contenido Instagram, 5) Scripts de ventas.",
        "categoria": "ejercicios"
    },
    {
        "id": "ejercicios_2",
        "texto": "Otros ejercicios: Secuencias de emails de seguimiento, análisis de competencia, planes de proyecto, artículos educativos, dashboards de métricas en Google Sheets.",
        "categoria": "ejercicios"
    },
    
    # Nicho de mercado
    {
        "id": "nicho_1",
        "texto": "Nichos objetivo: Restaurantes (reservas, pedidos, menú digital), Clínicas (citas, recordatorios, historial), Tiendas (atención, pedidos, inventario), Servicios profesionales (consultoría, agendamiento).",
        "categoria": "negocio"
    },
    {
        "id": "nicho_2",
        "texto": "Problemas comunes de las Pymes: Pierden pedidos por WhatsApp fuera de horario, no tienen presencia digital, pierden tiempo en tareas manuales, no hacen seguimiento a prospectos.",
        "categoria": "negocio"
    },
    
    # Propuestas
    {
        "id": "propuestas_1",
        "texto": "Estructura de propuesta: 1) Nombre del negocio, 2) Problema detectado, 3) Solución propuesta, 4) Servicios incluidos, 5) Próximos pasos, 6) Contacto. Formato: PDF profesional.",
        "categoria": "ventas"
    },
    {
        "id": "propuestas_2",
        "texto": "Precios sugeridos: Landing page $500,000-$1,500,000 COP, Chatbot WhatsApp $300,000-$800,000 COP, Automatización $500,000-$2,000,000 COP, Propuesta completa $200,000-$500,000 COP.",
        "categoria": "ventas"
    },
    
    # Hermes
    {
        "id": "hermes_1",
        "texto": "Hermes es un agente de IA que corre en la PC de Daniel. Está conectado a Discord como Comunicacion#7070. Usa el modelo llama3.2 de Ollama localmente.",
        "categoria": "tecnico"
    },
    {
        "id": "hermes_2",
        "texto": "Hermes puede: buscar en la web, ejecutar comandos, leer archivos, crear archivos, conectarse a Discord, y usar herramientas personalizadas. Está configurado con fallback a OpenRouter si Ollama falla.",
        "categoria": "tecnico"
    }
]

# Agregar documentos a la colección
for ctx in contextos:
    collection.add(
        documents=[ctx["texto"]],
        ids=[ctx["id"]],
        metadatas=[{"categoria": ctx["categoria"]}]
    )

print(f"Base de datos creada con {collection.count()} documentos")
print(f"Ubicación: {DB_PATH}")