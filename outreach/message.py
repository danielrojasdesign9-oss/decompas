"""Mensajes personalizados de outreach por lead (WhatsApp y Email)."""
from __future__ import annotations

import html


def build_whatsapp_message(lead: dict, report_url: str = "", owner: str = "") -> str:
    """Mensaje de WhatsApp con valor agregado (top 2 oportunidades detectadas)."""
    name = lead.get("name") or "tu negocio"
    city = lead.get("city") or "tu ciudad"
    score_data = lead.get("decompas_score") or {}
    score = score_data.get("score", 0)
    opps = score_data.get("opportunities", []) or []
    top2 = "\n".join(f"  • {o}" for o in opps[:2]) or "  • Oportunidades por detectar en un diagnóstico a fondo."

    report_link = report_url or "[Link al diagnóstico]"
    greeting = f"Hola {owner}, " if owner else "Hola, "

    return (
        f"{greeting}vi tu negocio en {city}. Analizamos la experiencia digital de {name} "
        f"y encontramos {min(2, len(opps)) if opps else 'detalles'} en el flujo de ventas donde "
        f"podrías estar perdiendo clientes frente a la competencia.\n\n"
        f"Puntos detectados:\n{top2}\n\n"
        f"Preparamos un diagnóstico rápido sin costo (puntaje {score}/100) aquí: {report_link}\n\n"
        "En DeCompas nos enfocamos en entender a fondo el negocio y resolverlo con IA y diseño."
    )


def build_email_message(lead: dict, report_url: str = "", owner: str = "") -> dict:
    """Email de outreach: asunto + cuerpo."""
    name = lead.get("name") or "tu negocio"
    city = lead.get("city") or "tu ciudad"
    score_data = lead.get("decompas_score") or {}
    score = score_data.get("score", 0)
    opps = score_data.get("opportunities", []) or []
    top2 = "\n".join(f"• {o}" for o in opps[:2]) or "• Oportunidades por detectar en un diagnóstico a fondo."
    report_link = report_url or "[Link al diagnóstico]"

    subject = f"Diagnóstico gratuito de {name} — ¿estás dejando clientes en la puerta?"
    body = (
        f"Hola{(' ' + owner) if owner else ''},\n\n"
        f"Vimos {name} en {city} y revisamos su presencia digital. El flujo de ventas móvil tiene "
        f"fugas concretas:\n\n{top2}\n\n"
        f"Preparamos un diagnóstico sin costo con puntaje {score}/100 y las acciones para mejorarlo: "
        f"{report_link}\n\n"
        "En DeCompas nos enfocamos en entender a fondo el negocio y resolverlo con IA y diseño, "
        "no vendemos 'páginas web' sino soluciones operativas.\n\n"
        "¿Agendamos 15 minutos esta semana?\n\nSaludos,\nDeCompas — Aliado de IA y diseño para Pymes\n"
        "https://decompas.netlify.app"
    )
    return {"subject": subject, "body": body}


def build_report_bundle(scored_leads: list[dict], base_url: str = "",
                        out_dir: str = "out") -> dict:
    """Genera mensajes para todos los leads. Devuelve diccionario para guardar."""
    bundle = []
    for lead in scored_leads:
        lead_id = lead.get("id") or ""
        report_url = f"{base_url}/{lead_id}.html" if (base_url and lead_id) else base_url
        wa = build_whatsapp_message(lead, report_url)
        email = build_email_message(lead, report_url)
        bundle.append({
            "id": lead_id,
            "name": lead.get("name", ""),
            "city": lead.get("city", ""),
            "whatsapp": lead.get("whatsapp", ""),
            "report_url": report_url,
            "message": wa,
            "email_subject": email["subject"],
            "email_body": email["body"],
        })
    return {"leads": bundle, "count": len(bundle)}
