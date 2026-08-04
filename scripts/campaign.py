"""Campaña semanal automática: leads -> DeCompas Score -> outreach -> deploy.

Uso (cada lunes via Programador de tareas):
  python scripts/campaign.py --city Cali --max 15

Qué hace:
  1. Busca leads en varios sectores de la ciudad (Places API o directorio).
  2. Audita cada lead (score 0-100).
  3. Rankea por mayor oportunidad: prioriza los que tienen WhatsApp y el
     score más bajo (peor presencia digital = más por ganar).
  4. Se queda con los `--max` mejores (mínimo 15 por defecto).
  5. Genera reportes HTML + mensajes + enlaces wa.me de un clic.
  6. Publica los reportes en Netlify (salvo --no-deploy) para que los
     enlaces del mensaje funcionen.

Fuentes de datos:
  --source api                  Places API (requiere GOOGLE_MAPS_API_KEY en .env)
  --source demo                 Datos de ejemplo (para probar el flujo)
  --source directory:<archivo>  Directorio público via config JSON
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except AttributeError:
    pass

DEFAULT_SECTORS = [
    "restaurantes",
    "salones de belleza",
    "gimnasios",
    "clínicas dentales",
    "veterinarias",
    "panaderías",
    "ferreterías",
    "abogados",
]
PER_SECTOR = 8
BASE_URL = "https://danielrojasdesign.netlify.app/diagnostico"


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Campaña semanal de prospección")
    p.add_argument("--city", default="Cali", help="Ciudad de búsqueda")
    p.add_argument("--max", type=int, default=15, help="Leads objetivo")
    p.add_argument("--sectors", default="", help="Sectores separados por coma (default: lista amplia)")
    p.add_argument("--source", default="auto",
                   help="auto | api | demo | scrape | directory:<config.json>")
    p.add_argument("--api-key", default="", help="Key de Places API (o GOOGLE_MAPS_API_KEY en .env)")
    p.add_argument("--region", default="", help="lat,lng,radius_m para acotar la zona")
    p.add_argument("--out-dir", default="out", help="Carpeta base de salida")
    p.add_argument("--no-deploy", action="store_true", help="No publicar reportes en Netlify")
    p.add_argument("--no-score", action="store_true", help="Saltar auditoría (solo leads)")
    return p


# ---------------------------------------------------------------- PASO 1: leads
def _fetch_api(args: argparse.Namespace, sectors: list) -> list:
    from leads.sources.google_maps import GoogleMapsSource
    api_key = args.api_key or load_from_env()
    if not api_key:
        return []
    src = GoogleMapsSource(api_key=api_key, default_country="57")
    leads, seen = [], set()
    for sector in sectors:
        try:
            for lead in src.fetch(sector, args.city, max_results=PER_SECTOR,
                                  region=args.region or None):
                key = (lead.name or "").strip().lower()
                if key and key not in seen:
                    seen.add(key)
                    leads.append(lead)
                    print(f"  [leads·api] {lead.name}")
        except Exception as e:
            print(f"  [warn] sector '{sector}': {e}")
        if len(leads) >= args.max * 3:
            break
    return leads


def _fetch_scrape(args: argparse.Namespace, sectors: list) -> list:
    from leads.sources.maps_scrape import MapsScrapeSource
    src = MapsScrapeSource(default_country="57", headless=True)
    leads, seen = [], set()
    for sector in sectors:
        try:
            for lead in src.fetch(sector, args.city, max_results=PER_SECTOR,
                                  max_per_sector=PER_SECTOR):
                key = (lead.name or "").strip().lower()
                if key and key not in seen:
                    seen.add(key)
                    leads.append(lead)
                    print(f"  [leads·scrape] {lead.name} | tel: {lead.phone}")
        except Exception as e:
            print(f"  [warn] sector '{sector}': {e}")
        if len(leads) >= args.max * 3:
            break
    return leads


def fetch_leads(args: argparse.Namespace) -> list:
    sectors = [s.strip() for s in args.sectors.split(",") if s.strip()] or DEFAULT_SECTORS

    if args.source == "demo":
        from leads.sources.demo import DemoSampleSource
        return list(DemoSampleSource("57").fetch())

    if args.source.startswith("directory:"):
        from leads.sources.directories import DirectorySource
        cfg = args.source.split(":", 1)[1]
        return list(DirectorySource(cfg, default_country="57").fetch())

    if args.source == "scrape":
        return _fetch_scrape(args, sectors)

    # auto / api
    from leads.sources.google_maps import load_from_env
    api_key = args.api_key or load_from_env()
    if args.source == "api" and not api_key:
        print("error: falta GOOGLE_MAPS_API_KEY. Pégala en .env (ver .env.example) "
              "o usa --source demo para probar.", file=sys.stderr)
        sys.exit(1)

    if api_key:
        try:
            leads = _fetch_api(args, sectors)
            if leads or args.source == "api":
                return leads
            print("  [warn] la API no devolvió leads; probando scraper ...")
        except Exception as e:
            print(f"  [warn] API falló ({e}); probando scraper ...")
    else:
        print("  [info] sin API key: usando scraper de Google Maps (respaldo)")

    return _fetch_scrape(args, sectors)


# ---------------------------------------------------------------- PASO 2: score
def score_leads(leads: list, out_path: str) -> list:
    from score.audit import audit

    scored = []
    for i, lead in enumerate(leads, 1):
        url = (lead.website or "").strip()
        print(f"  [score] {i}/{len(leads)}: {lead.name or url}")
        try:
            d = audit(url, with_mobile=False).to_dict()
        except Exception as e:
            print(f"    error: {e}")
            d = {"score": 0, "categories": {}, "opportunities": [],
                 "recommendations": [], "mobile": {}, "error": str(e)}
        row = lead.to_dict()
        row["decompas_score"] = d
        scored.append(row)

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(scored, f, ensure_ascii=False, indent=2)
    return scored


# ------------------------------------------------------- PASO 3: ranking
def rank_and_select(scored: list, target: int) -> list:
    """Mayor oportunidad primero: con WhatsApp y score más bajo."""
    def key(row):
        has_wa = 1 if (row.get("whatsapp") or "").strip() else 0
        return (has_wa, (row.get("decompas_score") or {}).get("score", 0))

    ranked = sorted(scored, key=key)
    selected = ranked[:target]
    print(f"  [rank] {len(selected)} seleccionados de {len(scored)} candidatos")
    for row in selected:
        s = (row.get("decompas_score") or {}).get("score", 0)
        wa = "si" if (row.get("whatsapp") or "").strip() else "NO"
        print(f"    - {row.get('name')} | score {s} | whatsapp: {wa}")
    return selected


# ------------------------------------------------- PASO 4: outreach + paquete
def build_outreach(scored: list, campaign_dir: str, base_url: str) -> str:
    from outreach.message import build_report_bundle
    from outreach.report import write_reports
    from urllib.parse import quote

    reports_dir = os.path.join(campaign_dir, "reports")
    write_reports(scored, out_dir=reports_dir)
    bundle = build_report_bundle(scored, base_url=base_url)

    msgs_path = os.path.join(campaign_dir, "outreach_messages.txt")
    with open(msgs_path, "w", encoding="utf-8") as f:
        for item in bundle["leads"]:
            f.write("=" * 66 + "\n")
            f.write(f"LEAD: {item['name']} | WhatsApp: {item['whatsapp']} | Reporte: {item['report_url']}\n")
            f.write("-" * 66 + "\n")
            f.write("[WHATSAPP]\n" + item["message"] + "\n\n")
            f.write("[EMAIL]\nAsunto: " + item["email_subject"] + "\n" + item["email_body"] + "\n\n")

    links_path = os.path.join(campaign_dir, "whatsapp_links.txt")
    with open(links_path, "w", encoding="utf-8") as f:
        for item in bundle["leads"]:
            wa_num = (item.get("whatsapp") or "").strip()
            link = f"https://wa.me/{wa_num}?text={quote(item['message'])}" if wa_num else "SIN WHATSAPP"
            f.write(f"{item['name']} | {link}\n")

    return msgs_path


def write_instructions(campaign_dir: str, city: str, count: int) -> None:
    with open(os.path.join(campaign_dir, "INSTRUCCIONES.txt"), "w", encoding="utf-8") as f:
        f.write(
            f"CAMPAÑA {city} · {count} leads · {datetime.now().strftime('%d/%m/%Y %H:%M')}\n"
            f"{'=' * 60}\n\n"
            "1. Abre 'whatsapp_links.txt'. Cada línea es un lead con su enlace de un clic.\n"
            "2. Haz clic: se abre WhatsApp Web con el mensaje listo. Revisa, personaliza\n"
            "   el nombre si hace falta y envía.\n"
            "3. Ritmo: 10-15 mensajes/día (lunes a miércoles). No envíes todos de golpe.\n"
            "4. Seguimiento a los 2-3 días a quien no respondió (réplica corta).\n"
            "5. Quien responda → agenda la revisión de dolores de 15 min.\n"
            "6. En la llamada: identifica dolores y, si hay fit, usa la calculadora\n"
            "   (danielrojasdesign.netlify.app) para mostrar el ROI y proponer sociedad.\n\n"
            "Los reportes por lead están publicados en:\n"
            f"  {BASE_URL}\n"
            "Métricas del día: revisa cuántos respondieron y qué sector funcionó mejor.\n"
        )


# ------------------------------------------------------- PASO 5: deploy reportes
def publish(campaign_dir: str, no_deploy: bool) -> None:
    reports = os.path.join(campaign_dir, "reports")
    if not os.path.isdir(reports):
        print("  [publish] no hay reportes que publicar")
        return
    if no_deploy:
        print("  [publish] omitido (--no-deploy)")
        return

    build = shutil.which("npm") and os.path.exists(os.path.join(ROOT, "package.json"))
    dist = os.path.join(ROOT, "dist")
    npm = shutil.which("npm.cmd") or "npm"
    npx = shutil.which("npx.cmd") or "npx"
    try:
        if build:
            print("  [publish] build dist/ ...")
            subprocess.run([npm, "run", "build"], cwd=ROOT, check=True,
                           capture_output=True, text=True, encoding="utf-8", errors="replace")
        else:
            os.makedirs(dist, exist_ok=True)
        target = os.path.join(dist, "diagnostico")
        shutil.rmtree(target, ignore_errors=True)
        shutil.copytree(reports, target)
        print(f"  [publish] reportes copiados a {target}")

        print("  [publish] deploy a Netlify ...")
        res = subprocess.run(
            [npx, "--yes", "netlify-cli", "deploy", "--prod", "--dir", dist],
            cwd=ROOT, capture_output=True, text=True, timeout=240,
            encoding="utf-8", errors="replace")
        print(res.stdout[-600:] if res.stdout else "")
        if res.returncode != 0:
            print("  [warn] deploy falló:", res.stderr[-400:])
    except Exception as e:
        print(f"  [warn] no se pudo publicar: {e}")


def main() -> int:
    args = build_parser().parse_args()
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    campaign_dir = os.path.join(args.out_dir, f"campaign_{args.city.replace(' ', '')}_{ts}")
    os.makedirs(campaign_dir, exist_ok=True)

    print(f"== CAMPAÑA | ciudad={args.city} | objetivo={args.max} | fuente={args.source} ==")
    print("[1/4] Buscando leads ...")
    leads = fetch_leads(args)
    if not leads:
        print("No se obtuvieron leads.", file=sys.stderr)
        return 1
    print(f"      {len(leads)} leads")

    leads_path = os.path.join(campaign_dir, "leads.json")
    with open(leads_path, "w", encoding="utf-8") as f:
        json.dump([l.to_dict() for l in leads], f, ensure_ascii=False, indent=2)

    if args.no_score:
        selected = [l.to_dict() for l in leads[:args.max]]
    else:
        print("[2/4] Auditando (score) ...")
        scored_path = os.path.join(campaign_dir, "scored.json")
        scored = score_leads(leads, scored_path)
        print("[3/4] Seleccionando por potencial ...")
        selected = rank_and_select(scored, args.max)

    print("[4/4] Generando reportes y mensajes ...")
    build_outreach(selected, campaign_dir, BASE_URL)
    write_instructions(campaign_dir, args.city, len(selected))
    publish(campaign_dir, args.no_deploy)

    print("\n" + "=" * 60)
    print(f"CAMPAÑA LISTA: {campaign_dir}")
    print(f"  - leads:            {os.path.join(campaign_dir, 'leads.json')}")
    print(f"  - mensajes:         {os.path.join(campaign_dir, 'outreach_messages.txt')}")
    print(f"  - enlaces un clic:  {os.path.join(campaign_dir, 'whatsapp_links.txt')}")
    print(f"  - instrucciones:    {os.path.join(campaign_dir, 'INSTRUCCIONES.txt')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
