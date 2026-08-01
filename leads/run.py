"""CLI del Lead Engine de DeCompas.

Ejemplos:
  python leads/run.py --source demo --output data/demo.json --csv
  python leads/run.py --source google_maps --query restaurantes --city Monterrey --max 50
  python leads/run.py --source google_maps --query "clínicas dentales" --city Guadalajara --scrape
  python leads/run.py --source directories --config directorio.json
"""
from __future__ import annotations

import argparse
import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except AttributeError:
    pass

from leads.export import export_csv, export_json  # noqa: E402
from leads.models import Lead  # noqa: E402
from leads.sources.demo import DemoSampleSource  # noqa: E402
from leads.sources.directories import DirectorySource  # noqa: E402
from leads.sources.google_maps import GoogleMapsSource, load_from_env  # noqa: E402


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Lead Engine de DeCompas (Paso A)")
    p.add_argument("--source", choices=["demo", "google_maps", "directories"], default="demo")
    p.add_argument("--query", default="", help="Tipo de negocio (ej. restaurantes)")
    p.add_argument("--city", default="", help="Ciudad / zona para acotar")
    p.add_argument("--max", type=int, default=50, help="Máximo de resultados")
    p.add_argument("--region", default="", help="lat,lng,radius_m para acotar (Places API)")
    p.add_argument("--api-key", default="", help="API key de Google Places (o GOOGLE_MAPS_API_KEY)")
    p.add_argument("--scrape", action="store_true", help="Usar scraping Playwright en vez de la API")
    p.add_argument("--config", default="", help="Ruta al JSON de configuración de directorios")
    p.add_argument("--country", default="57", help="Código de país por defecto (E.164, sin +)")
    p.add_argument("--no-enrich", action="store_true", help="No detectar redes sociales desde la web")
    p.add_argument("--output", default="", help="Archivo JSON de salida")
    p.add_argument("--csv", action="store_true", help="Además exportar CSV")
    p.add_argument("--out-dir", default="data")
    return p


def main() -> int:
    args = build_parser().parse_args()
    leads: list[Lead] = []

    if args.source == "demo":
        leads = list(DemoSampleSource(args.country).fetch())

    elif args.source == "google_maps":
        api_key = args.api_key or load_from_env()
        src = GoogleMapsSource(api_key=api_key, default_country=args.country)
        if args.scrape:
            if not args.query:
                print("error: --query es obligatorio para scraping", file=sys.stderr)
                return 1
            leads = list(src.fetch_scraped(args.query, args.city, max_results=args.max))
        else:
            if not api_key:
                print("error: falta GOOGLE_MAPS_API_KEY. Configúrala en .env o usa --api-key", file=sys.stderr)
                return 1
            leads = list(src.fetch(args.query, args.city, max_results=args.max, region=args.region or None))

    elif args.source == "directories":
        if not args.config:
            print("error: --config es obligatorio para directorios", file=sys.stderr)
            return 1
        leads = list(DirectorySource(args.config, default_country=args.country).fetch())

    if not args.no_enrich:
        from leads.enrich import enrich
        for i, lead in enumerate(leads):
            print(f"  [enrich] {i + 1}/{len(leads)}: {lead.name or lead.website}")
            leads[i] = enrich(lead)

    if not leads:
        print("No se obtuvieron leads.")
        return 1

    json_path = export_json(leads, out_dir=args.out_dir, filename=args.output or None)
    print(f"OK: {len(leads)} leads -> {json_path}")
    if args.csv:
        csv_path = export_csv(leads, out_dir=args.out_dir)
        print(f"OK: CSV -> {csv_path}")

    total_wa = sum(1 for l in leads if l.whatsapp)
    total_web = sum(1 for l in leads if l.website)
    total_redes = sum(1 for l in leads if l.social)
    print(f"Resumen: {len(leads)} leads | con WhatsApp: {total_wa} | con web: {total_web} | con redes: {total_redes}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
