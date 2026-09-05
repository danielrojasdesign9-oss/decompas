import discord
from discord.ext import commands, tasks
import requests
import json
import asyncio
import subprocess
import os
from datetime import datetime

# Configuración
TOKEN = os.getenv("DISCORD_BOT_TOKEN", "")
if not TOKEN:
    print("DISCORD_BOT_TOKEN no configurado. Exporta la variable de entorno.")
    print("   Ejemplo: $env:DISCORD_BOT_TOKEN='tu_token_aqui'")
WEBHOOK_URL = "http://localhost:8765"
CHANNEL_ID = 1544195974023352415  # Canal general

# Estado de OpenCode Web
opencode_process = None
OPENCODE_PORT = 4096

# Base de conocimiento - ideas
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IDEAS_FILE = os.path.join(BASE_DIR, "scripts", "soporte", "ideas.txt")
IDEAS_MIRROR = r"X:\Proyectos IA OpenCode\Entregables_Proyecto\soporte\ideas.txt"

def clasificar_idea(texto):
    t = texto.lower()
    if any(k in t for k in ["horario", "emergencia", "turno", "atienden", "abren", "cierran"]):
        return "horarios"
    if any(k in t for k in ["precio", "costo", "cobra", "pago", "anticipo", "cuota"]):
        return "precios"
    if any(k in t for k in ["menu", "catalogo", "producto", "plato", "pdf"]):
        return "catalogo"
    if any(k in t for k in ["reserva", "cita", "agenda", "turno"]):
        return "reservas"
    if any(k in t for k in ["estacionamiento", "parqueo", "ubicacion", "direccion", "donde"]):
        return "ubicacion"
    if any(k in t for k in ["faq", "pregunta frecuente", "siempre preguntan"]):
        return "faqs"
    if any(k in t for k in ["pedido", "domicilio", "entrega", "delivery"]):
        return "pedidos"
    if any(k in t for k in ["propuesta", "diagnostico", "auditoria", "template", "plantilla"]):
        return "templates"
    return "general"

def guardar_idea(texto):
    os.makedirs(os.path.dirname(IDEAS_FILE), exist_ok=True)
    ts = datetime.now().strftime("%Y-%m-%d %H:%M")
    cat = clasificar_idea(texto)
    linea = f"[{ts}] [{cat}] {texto}\n"
    with open(IDEAS_FILE, "a", encoding="utf-8") as f:
        f.write(linea)
    try:
        os.makedirs(os.path.dirname(IDEAS_MIRROR), exist_ok=True)
        with open(IDEAS_MIRROR, "a", encoding="utf-8") as f:
            f.write(linea)
    except Exception:
        pass
    return cat

# Bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Cola de mensajes pendientes
pending_messages = []

@bot.event
async def on_ready():
    print(f"Bot conectado como {bot.user}")
    check_webhook.start()

@tasks.loop(seconds=3)
async def check_webhook():
    """Revisa el webhook cada 3 segundos"""
    try:
        response = requests.get(WEBHOOK_URL)
        data = response.json()
        messages = data.get("messages", [])
        
        for msg in messages:
            if msg["source"] == "opencode":
                # Enviar al canal
                channel = bot.get_channel(CHANNEL_ID)
                if channel:
                    await channel.send(f"**OpenCode:** {msg['message']}")
                
                # Marcar como procesado
                requests.delete(WEBHOOK_URL, json={"id": msg["id"]})
                
    except Exception as e:
        pass

@bot.command(name="opencode")
async def opencode(ctx, *, mensaje):
    """Envía un mensaje a OpenCode y espera respuesta"""
    
    # Enviar mensaje a webhook
    try:
        requests.post(WEBHOOK_URL, json={
            "source": "hermes",
            "message": mensaje
        })
        
        await ctx.send("Procesando tu mensaje...")
            
    except Exception as e:
        await ctx.send(f"Error: {str(e)}")

@bot.command(name="status")
async def status(ctx):
    """Muestra el estado del sistema"""
    global opencode_process
    try:
        response = requests.get(WEBHOOK_URL)
        data = response.json()
        messages = data.get("messages", [])
        
        oc_status = "🟢 Encendido" if opencode_process and opencode_process.poll() is None else "🔴 Apagado"
        
        msg = f"**Estado del Sistema:**\n"
        msg += f"• Webhook: {'🟢 Activo' if True else '🔴 Inactivo'}\n"
        msg += f"• OpenCode Web: {oc_status}\n"
        msg += f"• Puerto: {OPENCODE_PORT}\n"
        msg += f"• Mensajes en cola: {len(messages)}\n"
        await ctx.send(msg)
    except Exception as e:
        await ctx.send(f"Error: {str(e)}")

@bot.command(name="encendido")
async def encendido(ctx):
    """Enciende el servidor de OpenCode Web en el puerto 4096"""
    global opencode_process
    
    channel = bot.get_channel(CHANNEL_ID)
    
    # Verificar si ya está corriendo
    if opencode_process and opencode_process.poll() is None:
        if channel:
            await channel.send(f"⚠️ **OpenCode Web** ya está corriendo en el puerto {OPENCODE_PORT}")
            await channel.send(f"📱 http://desktop-ide6st8:{OPENCODE_PORT}")
        return
    
    try:
        await ctx.send("🔄 Iniciando OpenCode Web...")
        
        # Iniciar el servidor en background (shell=True para encontrar opencode en PATH)
        opencode_process = subprocess.Popen(
            f"npx opencode-ai web --port {OPENCODE_PORT} --hostname 0.0.0.0",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True,
            creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
        )
        
        # Esperar un momento para que inicie
        await asyncio.sleep(4)
        
        if opencode_process.poll() is None:
            msg = f"🟢 **OpenCode Web ENCENDIDO** (sin contrasena)\n\n"
            msg += f"📱 **Celular (Tailscale):** http://desktop-ide6st8:{OPENCODE_PORT}\n"
            msg += f"💻 **PC:** http://localhost:{OPENCODE_PORT}\n"
            
            if channel:
                await channel.send(msg)
            await ctx.send(f"✅ OpenCode Web encendido — revisa el canal general")
        else:
            stderr = opencode_process.stderr.read().decode()
            await ctx.send(f"❌ Error al iniciar OpenCode Web")
            if stderr:
                await ctx.send(f"```{stderr[:200]}```")
            
    except FileNotFoundError:
        await ctx.send("❌ Error: OpenCode no está instalado. Ejecuta `npm install -g opencode-ai`")
    except Exception as e:
        await ctx.send(f"❌ Error: {str(e)}")

@bot.command(name="apagado")
async def apagado(ctx):
    """Apaga el servidor de OpenCode Web"""
    global opencode_process
    
    channel = bot.get_channel(CHANNEL_ID)
    
    if opencode_process is None or opencode_process.poll() is not None:
        if channel:
            await channel.send("ℹ️ **OpenCode Web** no está corriendo")
        return
    
    try:
        await ctx.send("🔄 Apagando OpenCode Web...")
        
        # Terminar el proceso
        opencode_process.terminate()
        
        # Esperar a que termine
        try:
            opencode_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            opencode_process.kill()
        
        opencode_process = None
        
        if channel:
            await channel.send(f"🔴 **OpenCode Web APAGADO** — Puerto {OPENCODE_PORT} liberado")
        await ctx.send("✅ OpenCode Web apagado")
        
    except Exception as e:
        await ctx.send(f"❌ Error al apagar: {str(e)}")

@bot.command(name="diagramas")
async def diagramas(ctx):
    """Muestra el enlace a los diagramas del flujo de ventas"""
    msg = f"📊 **Diagramas del Flujo de Ventas**\n\n"
    msg += f"Abre el HTML interactivo en tu navegador:\n"
    msg += f"📁 `scripts/diagramas/index.html`\n\n"
    msg += f"**Diagramas disponibles:**\n"
    msg += f"1. 🔍 Flujo Completo de Leads\n"
    msg += f"2. 🤝 Secuencia de Contacto\n"
    msg += f"3. 🌳 Decision Tree\n"
    msg += f"4. 📅 Timeline Semanal\n"
    await ctx.send(msg)

@bot.command(name="leads")
async def leads(ctx):
    """Muestra los scripts de ventas"""
    msg = f"📋 **Scripts de Ventas**\n\n"
    msg += f"📁 `scripts/leads/scripts_ventas.md`\n\n"
    msg += f"**Canales disponibles:**\n"
    msg += f"• LinkedIn (profesional)\n"
    msg += f"• WhatsApp (cercano)\n"
    msg += f"• Instagram (casual)\n"
    msg += f"• Grupos (público)\n"
    await ctx.send(msg)

@bot.command(name="propuesta")
async def propuesta(ctx):
    """Muestra el template de propuesta"""
    msg = f"📋 **Template de Propuesta**\n\n"
    msg += f"📁 `scripts/propuestas/propuesta_template.html`\n\n"
    msg += f"**Para generar PDF:**\n"
    msg += f"1. Abre el HTML en tu navegador\n"
    msg += f"2. Presiona Ctrl+P (Imprimir)\n"
    msg += f"3. Selecciona 'Guardar como PDF'\n"
    await ctx.send(msg)

@bot.command(name="idea")
async def idea(ctx, *, texto: str = ""):
    """Guarda una idea en tu base de conocimiento. Uso: !idea tu texto"""
    if not texto.strip():
        await ctx.send("Uso: `!idea tu idea aqui`\nEj: `!idea los clinicos piden horarios de emergencia`")
        return
    try:
        cat = guardar_idea(texto.strip())
        channel = bot.get_channel(CHANNEL_ID)
        msg = f"Idea guardada en tu base de conocimiento\nCategoria: **{cat}**\nTexto: {texto.strip()[:300]}"
        if channel and ctx.channel.id != CHANNEL_ID:
            await channel.send(msg)
        await ctx.send(msg)
    except Exception as e:
        await ctx.send(f"Error guardando idea: {str(e)}")

@bot.command(name="ideas")
async def ideas(ctx):
    """Muestra las ultimas 5 ideas guardadas"""
    try:
        if not os.path.exists(IDEAS_FILE):
            await ctx.send("Aun no hay ideas. Usa `!idea tu texto`")
            return
        with open(IDEAS_FILE, "r", encoding="utf-8") as f:
            lineas = [l.strip() for l in f if l.strip() and not l.startswith("#")]
        if not lineas:
            await ctx.send("Aun no hay ideas. Usa `!idea tu texto`")
            return
        ultimas = lineas[-5:]
        msg = "**Ultimas ideas:**\n" + "\n".join([f"- {l[:200]}" for l in ultimas])
        await ctx.send(msg[:1900])
    except Exception as e:
        await ctx.send(f"Error: {str(e)}")

# Ejecutar bot
if __name__ == "__main__":
    bot.run(TOKEN)