"""CLI del outreach de Daniel Rojas.

Ejemplo:
  python outreach/run_outreach.py --scored data/scored_20260801_001002.json \
      --base-url https://decompas-318.netlify.app/diagnostico --out-dir out
"""
from __future__ import annotations

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except AttributeError:
    pass

from outreach.message import build_report_bundle  # noqa: E402
from outreach.report import write_reports  # noqa: E402


def main() -> int:
    p = argparse.ArgumentParser(description="Outreach DeCompas: reportes + mensajes por lead")
    p.add_argument("--scored", required=True, help="JSON con leads ya auditados (salida de score/run_score.py)")
    p.add_argument("--base-url", default="https://decompas-318.netlify.app/diagnostico",
                   help="URL pública donde se publicarán los reportes")
    p.add_argument("--out-dir", default="out")
    args = p.parse_args()

    with open(args.scored, encoding="utf-8") as f:
        leads = json.load(f)

    reports_dir = os.path.join(args.out_dir, "reports")
    metas = write_reports(leads, out_dir=reports_dir)
    bundle = build_report_bundle(leads, base_url=args.base_url)

    msgs_path = os.path.join(args.out_dir, "outreach_messages.json")
    os.makedirs(args.out_dir, exist_ok=True)
    with open(msgs_path, "w", encoding="utf-8") as f:
        json.dump(bundle, f, ensure_ascii=False, indent=2)

    print(f"Reportes generados: {len(metas)} -> {reports_dir}")
    print(f"Mensajes generados: {bundle['count']} -> {msgs_path}")

    txt_path = os.path.join(args.out_dir, "outreach_messages.txt")
    with open(txt_path, "w", encoding="utf-8") as f:
        for item in bundle["leads"]:
            f.write("=" * 66 + "\n")
            f.write(f"LEAD: {item['name']} | WhatsApp: {item['whatsapp']} | Reporte: {item['report_url']}\n")
            f.write("-" * 66 + "\n")
            f.write("[WHATSAPP]\n" + item["message"] + "\n\n")
            f.write("[EMAIL]\nAsunto: " + item["email_subject"] + "\n" + item["email_body"] + "\n\n")
    print(f"Texto plano: -> {txt_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
