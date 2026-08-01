"""CLI del DeCompas Score (Paso B).

Ejemplos:
  python score/run_score.py --url https://decompas.netlify.app
  python score/run_score.py --lead data/demo_leads.json --out data/scored.json
  python score/run_score.py --whatsapp-probe 528112345678
  python score/run_score.py --whatsapp-check 528112345678
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except AttributeError:
    pass

from score.audit import audit  # noqa: E402
from score.whatsapp import check_probe, start_probe  # noqa: E402


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="DeCompas Score: diagnóstico IA de presencia digital")
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--url", help="URL de un sitio web a auditar")
    g.add_argument("--lead", help="Archivo JSON con leads (salida del Lead Engine)")
    g.add_argument("--whatsapp-probe", metavar="NUMERO", help="Inicia test de respuesta por WhatsApp")
    g.add_argument("--whatsapp-check", metavar="NUMERO", help="Evalúa tiempo de respuesta de un probe")
    p.add_argument("--message", default="", help="Mensaje del probe de WhatsApp")
    p.add_argument("--out", default="", help="Archivo JSON de salida")
    p.add_argument("--no-mobile", action="store_true", help="Omitir audit móvil con Playwright")
    return p


def print_report(lead_name: str, d: dict) -> None:
    score = d["score"]
    bar = "█" * (score // 5) + "░" * (20 - score // 5)
    print("\n" + "=" * 62)
    print(f"  DECOMPAS SCORE | {lead_name}")
    print(f"  {bar} {score}/100")
    print("=" * 62)
    for cat, val in d["categories"].items():
        maxv = {"presencia": 30, "diseno": 20, "conversion": 30, "seo": 20}[cat]
        label = {"presencia": "Presencia/rendimiento", "diseno": "Diseño responsivo",
                 "conversion": "Conversión/captura", "seo": "SEO/Accesibilidad"}[cat]
        print(f"  {label:<22} {val:>2}/{maxv}")
    if d["mobile"].get("load_time_s"):
        print(f"  Carga móvil: {d['mobile']['load_time_s']}s")
    if d["opportunities"]:
        print("\n  OPORTUNIDADES DE NEGOCIO:")
        for o in d["opportunities"]:
            print(f"   • {o}")
    if d["recommendations"]:
        print("\n  RECOMENDACIONES:")
        for r in d["recommendations"]:
            print(f"   • {r}")
    if d["error"]:
        print(f"\n  ERROR: {d['error']}")
    print("=" * 62 + "\n")


def main() -> int:
    args = build_parser().parse_args()

    if args.whatsapp_probe:
        path = start_probe(args.whatsapp_probe, args.message)
        print(f"Test iniciado. Envía este enlace (como prospecto) y avísale a la Pyme:\n  {json.load(open(path, encoding='utf-8'))['link']}")
        print("Luego corre: python score/run_score.py --whatsapp-check <numero>")
        return 0

    if args.whatsapp_check:
        print(json.dumps(check_probe(args.whatsapp_check), ensure_ascii=False, indent=2))
        return 0

    if args.url:
        d = audit(args.url, with_mobile=not args.no_mobile).to_dict()
        print_report(args.url, d)
        if args.out:
            with open(args.out, "w", encoding="utf-8") as f:
                json.dump(d, f, ensure_ascii=False, indent=2)
                print(f"Reporte guardado: {args.out}")
        return 0

    if args.lead:
        with open(args.lead, encoding="utf-8") as f:
            leads = json.load(f)
        scored = []
        for lead in leads:
            url = (lead.get("website") or "").strip()
            print(f"\n[score] {lead.get('name') or url}")
            d = audit(url, with_mobile=not args.no_mobile).to_dict()
            print_report(lead.get("name") or url, d)
            lead["decompas_score"] = d
            scored.append(lead)
        out = args.out or f"data/scored_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
        with open(out, "w", encoding="utf-8") as f:
            json.dump(scored, f, ensure_ascii=False, indent=2)
        print(f"\nListo: {len(scored)} leads auditados -> {out}")
        return 0

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
