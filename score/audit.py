"""Motor de auditoría del DeCompas Score.

Evalúa la presencia digital de una Pyme con heurísticas ligeras (requests +
BeautifulSoup) y opcionalmente un audit móvil real si Playwright está
instalado. Genera un puntaje 0-100 con 4 categorías:

  - Presencia digital y rendimiento (30)
  - Diseño y estética responsiva   (20)
  - Conversión y captura de leads  (30)
  - SEO y accesibilidad            (20)
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

CATEGORY_MAX = {
    "presencia": 30,
    "diseno": 20,
    "conversion": 30,
    "seo": 20,
}

CHAT_MARKERS = re.compile(
    r"intercom|tawk\.to|wow\.zopim|crisp\.chat|crisp-helpdesk|chatwoot|"
    r"zendesk|livechat|jivosite|getbutton|drift|fb\.com/plugins/messenger|"
    r"messenger\.js|widget\.getbutton|typebot|landbot|manychat",
    re.IGNORECASE,
)
GENERIC_TEMPLATE_MARKERS = re.compile(
    r"wix\.com|myshopify|cdn\.shopify|squarespace|webflow|elementor|"
    r"wp-content/themes/twentytwenty|jimdo|site123|carrd\.co|wordpress\.com",
    re.IGNORECASE,
)
CTA_WORDS = re.compile(
    r"cotiz(ar|a)|agend|reserv|compr(a|e|ar)|pedir|orden(ar|a)|contact|"
    r"llamar|whatsapp|más info|más información|solicitar",
    re.IGNORECASE,
)
WHATSAPP_RE = re.compile(r"(?:wa\.me|api\.whatsapp\.com/send)(?:[^\s\"']*?)(\d{7,15})", re.IGNORECASE)


@dataclass
class AuditResult:
    url: str
    has_site: bool
    reachable: bool = False
    checks: dict = field(default_factory=dict)
    score: int = 0
    categories: dict = field(default_factory=dict)
    opportunities: list[str] = field(default_factory=list)
    recommendations: list[str] = field(default_factory=list)
    mobile: dict = field(default_factory=dict)
    error: str = ""

    def to_dict(self) -> dict:
        return {
            "url": self.url,
            "has_site": self.has_site,
            "reachable": self.reachable,
            "checks": self.checks,
            "score": self.score,
            "categories": self.categories,
            "opportunities": self.opportunities,
            "recommendations": self.recommendations,
            "mobile": self.mobile,
            "error": self.error,
        }


def _pick(url: str) -> str:
    url = (url or "").strip()
    if not url:
        return ""
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    return url


def audit(url: str, with_mobile: bool = True, timeout: int = 20) -> AuditResult:
    """Ejecuta la auditoría completa sobre una URL."""
    url = _pick(url)
    result = AuditResult(url=url, has_site=bool(url))
    if not url:
        result.opportunities.append("No tiene sitio web: oportunidad de crear su ecosistema digital desde cero.")
        result.recommendations.append("Proponer creación de landing/ecosistema digital con identidad de marca y chat de ventas.")
        result = _score(result)
        return result

    try:
        resp = requests.get(url, timeout=timeout,
                            headers={"User-Agent": "Mozilla/5.0 (DeCompas-Auditor/1.0)"})
        result.reachable = True
    except requests.RequestException as e:
        result.error = f"Error al cargar {url}: {e}"
        result.opportunities.append("El sitio no responde o está caído: se pierden clientes desde el primer contacto.")
        result.recommendations.append("Revisar hosting/uptime; garantizar HTTPS y tiempos de carga < 2.5s.")
        result = _score(result)
        return result

    html = resp.text
    soup = BeautifulSoup(html, "html.parser")
    load_s = resp.elapsed.total_seconds()

    checks: dict = {
        "https": url.startswith("https://"),
        "load_time_s": round(load_s, 2),
        "page_kb": round(len(html) / 1024, 1),
        "status_code": resp.status_code,
        "viewport": bool(soup.find("meta", attrs={"name": "viewport"})),
        "lang": bool(soup.html and soup.html.get("lang")),
        "title": bool(soup.title and soup.title.string and soup.title.string.strip()),
        "meta_description": bool(soup.find("meta", attrs={"name": "description"})),
        "og_tags": bool(soup.find("meta", attrs={"property": re.compile(r"og:"), "content": True})),
        "generator": (soup.find("meta", attrs={"name": "generator"}) or {}).get("content", "")
                     if soup.find("meta", attrs={"name": "generator"}) else "",
        "images": len(soup.find_all("img")),
        "images_without_alt": sum(1 for img in soup.find_all("img") if not img.get("alt")),
        "scripts": len(soup.find_all("script", src=True)),
        "stylesheets": len(soup.find_all("link", rel="stylesheet")),
        "forms": len(soup.find_all("form")),
        "tel_links": len(soup.find_all("a", href=re.compile(r"^tel:"))),
        "whatsapp_links": len(soup.find_all("a", href=re.compile(r"wa\.me|whatsapp\.com/send", re.IGNORECASE))),
        "cta_links": 0,
    }

    cta = 0
    for a in soup.find_all("a"):
        text = " ".join(a.stripped_strings)
        href = a.get("href") or ""
        if CTA_WORDS.search(text) or CTA_WORDS.search(href):
            cta += 1
    checks["cta_links"] = cta

    text = re.sub(r"\s+", " ", html.lower())
    checks["chat_widget"] = bool(CHAT_MARKERS.search(text))
    checks["generic_template"] = bool(GENERIC_TEMPLATE_MARKERS.search(text))
    wa_match = WHATSAPP_RE.search(html)
    checks["whatsapp_number"] = re.sub(r"[^\d]", "", wa_match.group(1)) if wa_match else ""

    # media queries = señal de diseño responsivo (heurística)
    checks["media_queries"] = len(re.findall(r"@media", html))

    result.checks = checks
    if with_mobile:
        result.mobile = _mobile_audit(url, timeout)

    result = _score(result)
    return result


def _mobile_audit(url: str, timeout: int) -> dict:
    """Audit móvil real (carga + viewport) si Playwright está disponible."""
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        return {"note": "Playwright no instalado; audit móvil omitido (pip install playwright)"}

    out: dict = {}
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        ctx = browser.new_context(viewport={"width": 390, "height": 844}, is_mobile=True)
        page = ctx.new_page()
        start = __import__("time").time()
        try:
            page.goto(url, timeout=timeout * 1000, wait_until="domcontentloaded")
            load = __import__("time").time() - start
            out["load_time_s"] = round(load, 2)
            out["title"] = page.title()
            out["has_overflow_x"] = page.evaluate(
                "() => document.documentElement.scrollWidth > document.documentElement.clientWidth"
            )
            out["tap_targets"] = page.evaluate(
                "() => { let bad=0; document.querySelectorAll('a,button').forEach(e=>{"
                " const r=e.getBoundingClientRect(); if(r.height<40||r.width<40) bad++;}); return bad; }"
            )
        except Exception as e:
            out["error"] = str(e)
        finally:
            browser.close()
    return out


def _score(result: AuditResult) -> AuditResult:
    checks = result.checks
    cat = {k: 0 for k in CATEGORY_MAX}

    # --- Presencia y rendimiento (30) ---
    if result.has_site:
        cat["presencia"] += 20
        if checks.get("https"):
            cat["presencia"] += 5
        if checks.get("load_time_s", 99) < 2.5:
            cat["presencia"] += 5
        else:
            result.recommendations.append("Carga > 2.5s: optimizar imágenes, comprimir HTML/CSS/JS.")
    else:
        cat["presencia"] = 0

    # --- Diseño y estética (20) ---
    if result.has_site and result.reachable:
        if checks.get("viewport"):
            cat["diseno"] += 10
            result.checks["responsive"] = True
        else:
            result.recommendations.append("Falta viewport meta: el sitio no se ve bien en móviles.")
        if checks.get("media_queries", 0) > 0:
            cat["diseno"] += 5
        if not checks.get("generic_template"):
            cat["diseno"] += 5
        else:
            result.opportunities.append("Detectada plantilla genérica: riesgo de estética de IA/estándar sin diferenciación.")
            result.recommendations.append("Rediseño con identidad de marca (frontend-design-system) y tipografía profesional.")

    # --- Conversión y captura (30) ---
    if result.has_site and result.reachable:
        if checks.get("whatsapp_links", 0) > 0 or checks.get("whatsapp_number"):
            cat["conversion"] += 10
        else:
            result.opportunities.append("Sin botón de WhatsApp: los prospectos no pueden contactar en 1 clic.")
            result.recommendations.append("Agregar botón de WhatsApp con saludo automático.")
        if checks.get("chat_widget"):
            cat["conversion"] += 10
        else:
            result.opportunities.append("Sin chat/asistente de ventas: los leads se pierden fuera de horario.")
            result.recommendations.append("Implementar agente de atención 24/7 (chat de ventas con IA).")
        if checks.get("cta_links", 0) >= 2 or checks.get("forms", 0) >= 1 or checks.get("tel_links", 0) >= 1:
            cat["conversion"] += 10
        else:
            result.recommendations.append("Faltan llamados a la acción claros (cotizar, agendar, pedir).")

    # --- SEO y accesibilidad (20) ---
    if result.has_site and result.reachable:
        if checks.get("title"):
            cat["seo"] += 5
        if checks.get("meta_description"):
            cat["seo"] += 3
        if checks.get("og_tags"):
            cat["seo"] += 2
        else:
            result.recommendations.append("Faltan Open Graph tags para compartir bien en WhatsApp/redes.")
        if checks.get("lang"):
            cat["seo"] += 5
        if checks.get("images", 0) > 0:
            alt_ratio = 1 - (checks.get("images_without_alt", 0) / checks["images"])
            cat["seo"] += 5 if alt_ratio >= 0.9 else 3 if alt_ratio >= 0.5 else 0
            if alt_ratio < 0.5:
                result.recommendations.append("Imágenes sin alt text: perjudica SEO y accesibilidad.")

    total = int(sum(cat.values()))
    result.categories = cat
    result.score = total

    if total >= 80:
        result.recommendations.append("Presencia digital sólida: proponer optimización y automatización avanzada (Fractional AI & Design Officer).")
    elif total >= 50:
        result.recommendations.append("Buen punto de partida: hay fugas de conversión concretas por cerrar.")
    else:
        result.recommendations.append("Oportunidad mayor: intervención integral de IA y diseño.")

    return result
