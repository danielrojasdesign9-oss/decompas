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
    print("⚠️ DISCORD_BOT_TOKEN no configurado. Exporta la variable de entorno.")
    print("   Ejemplo: $env:DISCORD_BOT_TOKEN='tu_token_aqui'")
WEBHOOK_URL = "http://localhost:8765"
CHANNEL_ID = 1544195974023352415  # Canal general

# Estado de OpenCode Web
opencode_process = None
OPENCODE_PORT = 4096

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
    
    # Verificar si ya está corriendo
    if opencode_process and opencode_process.poll() is None:
        await ctx.send(f"⚠️ OpenCode Web ya está corriendo en el puerto {OPENCODE_PORT}")
        await ctx.send(f"📱 Accede desde tu celular: http://desktop-ide6st8:{OPENCODE_PORT}")
        return
    
    try:
        await ctx.send("🔄 Iniciando OpenCode Web...")
        
        # Iniciar el servidor en background (shell=True para encontrar opencode en PATH)
        opencode_process = subprocess.Popen(
            f"opencode web --port {OPENCODE_PORT} --host 0.0.0.0",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True,
            creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
        )
        
        # Esperar un momento para que inicie
        await asyncio.sleep(4)
        
        if opencode_process.poll() is None:
            await ctx.send(f"✅ **OpenCode Web encendido**")
            await ctx.send(f"📱 **Desde tu celular (Tailscale):** http://desktop-ide6st8:{OPENCODE_PORT}")
            await ctx.send(f"💻 **Desde tu PC:** http://localhost:{OPENCODE_PORT}")
            await ctx.send(f"🔑 **Usuario:** danielremoto")
            await ctx.send(f"🔐 **Contraseña:** makiMa12*")
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
    
    if opencode_process is None or opencode_process.poll() is not None:
        await ctx.send("ℹ️ OpenCode Web no está corriendo")
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
        
        await ctx.send("✅ **OpenCode Web apagado**")
        await ctx.send(f"🔌 Puerto {OPENCODE_PORT} liberado")
        
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

# Ejecutar bot
if __name__ == "__main__":
    bot.run(TOKEN)