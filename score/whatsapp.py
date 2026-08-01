"""Prueba de tiempo de respuesta por WhatsApp (simulación de prospecto).

El test es semimanual: `--whatsapp-probe` genera el enlace wa.me con un
mensaje prefabricado y registra la hora de inicio. El operador envía el
mensaje y `--whatsapp-check` calcula cuánto tardaron en responder para
calificar la oportunidad de un Agente MCP de Automatización de Ventas.
"""
from __future__ import annotations

import json
import os
import time
from datetime import datetime, timezone
from urllib.parse import quote

STATE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "wa_probes")
THRESHOLD_MIN = 15  # 15 minutos como límite aceptable
DEFAULT_MESSAGE = "Hola, ¿siguen atendiendo? Me gustaría pedir una cotización, ¿me pueden apoyar?"


def _state_path(number: str) -> str:
    os.makedirs(STATE_DIR, exist_ok=True)
    return os.path.join(STATE_DIR, f"{number}.json")


def build_probe_link(number: str, message: str = DEFAULT_MESSAGE) -> str:
    digits = "".join(ch for ch in number if ch.isdigit())
    return f"https://wa.me/{digits}?text={quote(message)}"


def start_probe(number: str, message: str = DEFAULT_MESSAGE) -> str:
    """Registra el inicio del test y devuelve el enlace wa.me a enviar."""
    path = _state_path(number)
    with open(path, "w", encoding="utf-8") as f:
        json.dump({"number": number, "start": time.time(),
                   "start_iso": datetime.now(timezone.utc).isoformat(),
                   "message": message, "link": build_probe_link(number, message)}, f)
    return path


def check_probe(number: str) -> dict:
    """Evalúa el tiempo transcurrido desde el inicio del test."""
    path = _state_path(number)
    if not os.path.exists(path):
        return {"error": "No hay test iniciado para ese número. Usa --whatsapp-probe primero."}
    with open(path, encoding="utf-8") as f:
        state = json.load(f)
    elapsed_min = round((time.time() - state["start"]) / 60, 1)
    fast = elapsed_min <= THRESHOLD_MIN
    return {
        "number": number,
        "link": state["link"],
        "elapsed_min": elapsed_min,
        "threshold_min": THRESHOLD_MIN,
        "responds_fast": fast,
        "opportunity": not fast,
        "recommendation": (
            "Responden rápido: WhatsApp no es urgencia; enfocar venta en web/conversión."
            if fast else
            "Tardan más de 15 min: oportunidad de Agente MCP de Automatización de Ventas (respuesta 24/7)."
        ),
    }
