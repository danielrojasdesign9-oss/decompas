"""Generador de reportes HTML personalizados por lead (DeCompas Score).

Cada reporte es una página autocontenida (CSS inline) con la identidad de
Daniel Rojas, lista para abrir localmente o publicar en la web.
"""
from __future__ import annotations

import html
import os

CATEGORY_LABELS = {
    "presencia": ("Presencia digital", "30"),
    "diseno": ("Diseño responsivo", "20"),
    "conversion": ("Conversión y captura", "30"),
    "seo": ("SEO y accesibilidad", "20"),
}
CATEGORY_ORDER = ["presencia", "diseno", "conversion", "seo"]

CSS = """
:root{--ink:#16222e;--muted:#5b6b7c;--cream:#faf7f2;--card:#ffffff;--amber:#e07b39;
--amber-soft:#fdeee2;--green:#2e7d5b;--red:#c0403a;--line:#e9e2d7;}
*{box-sizing:border-box;margin:0;padding:0;}
body{font-family:'Inter',-apple-system,'Segoe UI',Roboto,sans-serif;background:var(--cream);
color:var(--ink);line-height:1.55;-webkit-font-smoothing:antialiased;}
.serif{font-family:'Fraunces',Georgia,serif;}
.wrap{max-width:760px;margin:0 auto;padding:40px 20px 80px;}
.brand{display:flex;align-items:center;gap:10px;font-weight:800;letter-spacing:.02em;font-size:1.05rem;}
.brand .dot{width:12px;height:12px;border-radius:3px;background:var(--amber);}
.hero{background:var(--card);border:1px solid var(--line);border-radius:18px;padding:34px 30px;margin-top:26px;
box-shadow:0 10px 30px rgba(22,34,46,.06);}
.tag{display:inline-block;background:var(--amber-soft);color:var(--amber);font-size:.72rem;font-weight:700;
text-transform:uppercase;letter-spacing:.08em;padding:5px 10px;border-radius:999px;}
h1{font-size:2rem;line-height:1.15;margin:14px 0 6px;}
.meta{color:var(--muted);font-size:.92rem;margin-bottom:22px;}
.scorebar{display:flex;align-items:center;gap:20px;flex-wrap:wrap;}
.ring{position:relative;width:120px;height:120px;flex:none;}
.ring svg{transform:rotate(-90deg);}
.ring .num{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;
font-size:1.9rem;font-weight:800;}
.scorelab{font-size:.78rem;color:var(--muted);}
.cats{flex:1;min-width:220px;display:grid;gap:10px;}
.cat{display:grid;grid-template-columns:1fr auto;font-size:.86rem;gap:4px 12px;}
.cat b{font-weight:600;}
.track{grid-column:1/-1;height:8px;background:var(--line);border-radius:99px;overflow:hidden;}
.fill{height:100%;border-radius:99px;background:var(--amber);}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:18px;margin-top:26px;}
@media(max-width:640px){.grid{grid-template-columns:1fr;}}
.card{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:22px;}
.card h3{font-size:1rem;margin-bottom:14px;display:flex;align-items:center;gap:8px;}
.card ul{list-style:none;display:grid;gap:10px;}
.card li{font-size:.9rem;color:#2a3644;padding-left:22px;position:relative;}
.card li::before{position:absolute;left:0;top:0;content:"•";font-weight:800;}
.opp li::before{color:var(--red);}
.rec li::before{color:var(--green);}
.cta{display:block;text-align:center;margin-top:28px;background:var(--ink);color:#fff;text-decoration:none;
padding:16px 22px;border-radius:12px;font-weight:700;font-size:1rem;transition:transform .15s;}
.cta:hover{transform:translateY(-2px);}
.wa{background:#25d366;color:#062b16;}
.sub{text-align:center;color:var(--muted);font-size:.85rem;margin-top:14px;}
.foot{margin-top:46px;text-align:center;color:var(--muted);font-size:.82rem;}
.foot a{color:var(--amber);font-weight:600;text-decoration:none;}
.err{background:#fdeeee;border:1px solid #f3c6c4;color:var(--red);border-radius:12px;padding:14px 16px;
font-size:.9rem;margin-top:20px;}
"""


def _score_color(score: int) -> str:
    if score >= 80:
        return "var(--green)"
    if score >= 50:
        return "var(--amber)"
    return "var(--red)"


def _ring(score: int) -> str:
    pct = score
    color = _score_color(score)
    r = 52
    c = 2 * 3.14159 * r
    return f"""
    <div class="ring">
      <svg width="120" height="120" viewBox="0 0 120 120">
        <circle cx="60" cy="60" r="{r}" fill="none" stroke="#e9e2d7" stroke-width="12"/>
        <circle cx="60" cy="60" r="{r}" fill="none" stroke="{color}" stroke-width="12"
          stroke-linecap="round" stroke-dasharray="{c}" stroke-dashoffset="{c * (1 - pct / 100)}"/>
      </svg>
      <div class="num">{score}</div>
    </div>"""


def _category_row(key: str, value: int) -> str:
    label, maxv = CATEGORY_LABELS[key]
    pct = min(100, int(value / int(maxv) * 100))
    return f"""
    <div class="cat">
      <b>{html.escape(label)}</b><span>{value}/{maxv}</span>
      <div class="track"><div class="fill" style="width:{pct}%"></div></div>
    </div>"""


def build_report_html(lead: dict, report_path: str = "", base_url: str = "") -> str:
    """Genera la página HTML del reporte de un lead ya auditado."""
    name = lead.get("name") or "Tu negocio"
    score_data = lead.get("decompas_score") or {}
    score = int(score_data.get("score", 0))
    categories = score_data.get("categories", {})
    opps = score_data.get("opportunities", []) or []
    recs = score_data.get("recommendations", []) or []
    error = score_data.get("error", "")
    mobile = score_data.get("mobile", {})
    city = lead.get("city", "")
    category = lead.get("category", "")

    cat_rows = "\n".join(_category_row(k, categories.get(k, 0)) for k in CATEGORY_ORDER)
    opp_items = "\n".join(f"<li>{html.escape(o)}</li>" for o in opps) or "<li>Sin oportunidades detectadas.</li>"
    rec_items = "\n".join(f"<li>{html.escape(r)}</li>" for r in recs) or "<li>Sin recomendaciones.</li>"
    err_html = f'<div class="err">⚠ {html.escape(error)}</div>' if error else ""

    mobile_line = ""
    if mobile.get("load_time_s"):
        mobile_line = f"<p class='meta'>Carga móvil: {mobile['load_time_s']}s</p>"

    wa = (lead.get("whatsapp_url") or lead.get("whatsapp") or "").strip()
    wa_num = (lead.get("whatsapp") or "").strip()
    wa_url = f"https://wa.me/{wa_num}?text={quote_text('Hola Daniel, vi el diagnóstico de mi negocio. ¿Cómo puedo mejorar mi puntaje?')}" if wa_num else ""
    cta_wa = f'<a class="cta wa" href="{wa_url}" target="_blank" rel="noopener">Quiero mejorar mi puntaje →</a>' if wa_url else ""
    cta_main = f'<a class="cta" href="{base_url}" target="_blank" rel="noopener">Quiero el diagnóstico completo en DeCompas</a>'

    sub = f"<p class='sub'>Reporte preparado por DeCompas · {city} · {category}</p>" if (city or category) else ""

    title = html.escape(f"{name} — Diagnóstico IA")
    return f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>{title}</title>
<style>{CSS}</style>
</head>
<body>
<div class="wrap">
  <div class="brand"><span class="dot"></span>DANIEL ROJAS<span style="color:var(--muted);font-weight:500">/diagnóstico</span></div>
  <div class="hero">
    <span class="tag">Diagnóstico IA de tu negocio</span>
    <h1 class="serif">{html.escape(name)}</h1>
    {mobile_line}
    {sub}
    <div class="scorebar">
      {_ring(score)}
      <div class="cats">{cat_rows}</div>
    </div>
    {err_html}
  </div>
  <div class="grid">
    <div class="card opp"><h3 class="serif">Oportunidades para tu negocio</h3><ul>{opp_items}</ul></div>
    <div class="card rec"><h3 class="serif">Qué recomendamos hacer</h3><ul>{rec_items}</ul></div>
  </div>
  {cta_wa}
  {cta_main}
  <div class="foot">
    <p>Consultor de IA y Diseño para Pymes · <a href="https://decompas-318.netlify.app">decompas-318.netlify.app</a></p>
    <p style="margin-top:6px">Auditoría de procesos primero, código después.</p>
  </div>
</div>
</body>
</html>"""


def quote_text(text: str) -> str:
    from urllib.parse import quote
    return quote(text)


def write_reports(scored_leads: list[dict], out_dir: str = "out/reports") -> list[dict]:
    """Escribe un reporte HTML por lead y un índice. Devuelve metadatos de reportes."""
    os.makedirs(out_dir, exist_ok=True)
    index_rows = []
    metas = []
    for lead in scored_leads:
        lead_id = lead.get("id") or f"{len(metas) + 1:04d}"
        fname = f"{lead_id}.html"
        path = os.path.join(out_dir, fname)
        with open(path, "w", encoding="utf-8") as f:
            f.write(build_report_html(lead, report_path=fname))
        metas.append({"id": lead_id, "file": fname, "path": path,
                      "name": lead.get("name", ""), "score": (lead.get("decompas_score") or {}).get("score", 0)})
        score = (lead.get("decompas_score") or {}).get("score", 0)
        index_rows.append(
            f'<tr><td><a href="{fname}">{html.escape(lead.get("name", ""))}</a></td>'
            f'<td>{html.escape(lead.get("city", ""))}</td>'
            f'<td><b>{score}</b></td></tr>'
        )
    index_html = f"""<!DOCTYPE html><html lang="es"><head><meta charset="utf-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>Diagnósticos DeCompas</title>
<style>body{{font-family:system-ui,sans-serif;background:#faf7f2;color:#16222e;max-width:820px;margin:0 auto;padding:40px 20px}}
table{{width:100%;border-collapse:collapse;background:#fff;border-radius:14px;overflow:hidden}}
th,td{{padding:12px 16px;text-align:left;border-bottom:1px solid #e9e2d7}}
th{{background:#16222e;color:#fff;font-size:.85rem}}
a{{color:#e07b39;font-weight:600;text-decoration:none}}</style></head>
<body><h1>Diagnósticos DeCompas</h1><p style="color:#5b6b7c">Reportes generados para tu outreach</p>
<table><tr><th>Negocio</th><th>Ciudad</th><th>Score</th></tr>{''.join(index_rows)}</table></body></html>"""
    with open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(index_html)
    return metas
