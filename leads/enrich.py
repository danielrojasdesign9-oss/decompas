"""Enriquecimiento: detecta redes sociales y botón de WhatsApp desde la web."""
from __future__ import annotations

import re
from urllib.parse import urljoin

import requests

from .models import Lead

SOCIAL_PATTERNS = {
    "facebook": r"(?:https?://(?:www\.)?facebook\.com/[A-Za-z0-9_.\-]+)",
    "instagram": r"(?:https?://(?:www\.)?instagram\.com/[A-Za-z0-9_.\-]+)",
    "tiktok": r"(?:https?://(?:www\.)?tiktok\.com/@[A-Za-z0-9_.\-]+)",
    "x": r"(?:https?://(?:www\.)?x\.com/[A-Za-z0-9_]+)",
    "linkedin": r"(?:https?://(?:www\.)?linkedin\.com/(?:company|in)/[A-Za-z0-9\-]+)",
}
WHATSAPP_RE = re.compile(r"(?:wa\.me|api\.whatsapp\.com/send)(?:[^\s\"']*?)(\d{7,15})", re.IGNORECASE)


def fetch_social_links(website: str, timeout: int = 15) -> dict:
    """Descarga el sitio y extrae enlaces a redes sociales y WhatsApp."""
    social: dict = {}
    if not website:
        return social
    try:
        resp = requests.get(website, timeout=timeout,
                            headers={"User-Agent": "Mozilla/5.0 (DeCompas-LeadEngine/1.0)"})
        resp.raise_for_status()
    except requests.RequestException:
        return social

    html = resp.text
    for platform, pattern in SOCIAL_PATTERNS.items():
        for match in re.finditer(pattern, html):
            url = match.group(0).rstrip("/")
            social.setdefault(platform, url)
            break  # solo el primer enlace por plataforma

    wa = WHATSAPP_RE.search(html)
    if wa:
        social["whatsapp_on_site"] = f"https://wa.me/{re.sub(r'[^\d]', '', wa.group(1))}"
    return social


def enrich(lead: Lead, with_social: bool = True, timeout: int = 15) -> Lead:
    """Completa el lead con presencia social detectada en su sitio web."""
    if with_social and lead.website:
        social = fetch_social_links(lead.website, timeout=timeout)
        if social:
            merged = dict(lead.social)
            merged.update(social)
            lead.social = merged
    return lead
