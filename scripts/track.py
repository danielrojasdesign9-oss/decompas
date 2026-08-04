"""Tracker de seguimiento de casos (mini-CRM local).

Cada campaña genera leads; aquí se les hace seguimiento caso a caso:
estado actual, próxima acción y fecha, y el embudo (ventas/socios).

Uso:
  python scripts/track.py seed --from <carpeta_campana>   # importa una campaña
  python scripts/track.py list                            # todos los leads
  python scripts/track.py list --status llamada           # filtra por estado
  python scripts/track.py update <id|"nombre"> --status socio --note "Firmó retainer"
  python scripts/track.py today                           # seguimientos de hoy
  python scripts/track.py next <id|"nombre">              # próxima acción de un caso
  python scripts/track.py stats                           # embudo
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import date, timedelta

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CRM_PATH = os.path.join(ROOT, "data", "crm.json")

STATUSES = {
    "enviado":        "Mensaje enviado, esperando respuesta",
    "respondio":      "Respondió: agendar llamada de 15 min",
    "llamada":        "Llamada hecha: preparar propuesta",
    "propuesta":      "Propuesta/contrato enviado",
    "socio":          "Socio aliado (genera proyectos)",
    "no_interesado":  "Cerrado: no interesado",
    "no_responde":    "Cerrado: no respondió (2+ réplicas)",
}
CLOSED = {"socio", "no_interesado", "no_responde"}

# días que se espera para la próxima acción según el estado
GAP_DAYS = {"enviado": 2, "llamada": 1, "propuesta": 3, "respondio": 0}
ACTION_TEXT = {
    "enviado":       "Seguimiento (réplica corta: el reporte sigue disponible)",
    "respondio":     "AGENDAR llamada de 15 min (revisión de dolores) — hoy mismo",
    "llamada":       "Enviar propuesta + contrato",
    "propuesta":     "Seguimiento de propuesta",
    "socio":         "Cerrado con éxito: mantener relación y buscar nuevos proyectos",
    "no_interesado": "Cerrado",
    "no_responde":   "Cerrado",
}


def _load() -> list:
    if not os.path.exists(CRM_PATH):
        return []
    with open(CRM_PATH, encoding="utf-8") as f:
        return json.load(f)


def _save(leads: list) -> None:
    os.makedirs(os.path.dirname(CRM_PATH), exist_ok=True)
    with open(CRM_PATH, "w", encoding="utf-8") as f:
        json.dump(leads, f, ensure_ascii=False, indent=2)


def _today() -> str:
    return date.today().isoformat()


def _fmt(d: str) -> str:
    return "/".join(reversed(d.split("-"))) if d else "-"


def _next_action(lead: dict) -> tuple:
    status = lead.get("status", "enviado")
    last = lead.get("last_update") or _today()
    gap = GAP_DAYS.get(status, 0)
    due = (date.fromisoformat(last) + timedelta(days=gap)).isoformat()
    return due, ACTION_TEXT.get(status, "Seguimiento")


def _match(leads: list, key: str) -> list:
    key = key.strip().lower()
    out = []
    for l in leads:
        if key == str(l.get("id")).lower() or key == (l.get("name") or "").lower():
            out.append(l)
    for l in leads:
        if key in (l.get("name") or "").lower():
            out.append(l)
    return out


# ---------------------------------------------------------------- comandos
def cmd_seed(args) -> None:
    campaign = args.from_dir
    scored = os.path.join(campaign, "scored.json")
    leads_path = scored if os.path.exists(scored) else os.path.join(campaign, "leads.json")
    if not os.path.exists(leads_path):
        print(f"error: no existe {leads_path}", file=sys.stderr)
        return 1
    with open(leads_path, encoding="utf-8") as f:
        rows = json.load(f)

    crm = _load()
    known = {(l.get("name") or "").strip().lower(): l for l in crm}
    day = _today()
    added = updated = 0
    for r in rows:
        name = (r.get("name") or "").strip()
        if not name:
            continue
        key = name.lower()
        score = (r.get("decompas_score") or {}).get("score", 0) if isinstance(r.get("decompas_score"), dict) else 0
        if key in known:
            known[key]["campaign"] = os.path.basename(campaign)
            known[key]["score"] = score
            updated += 1
            continue
        crm.append({
            "id": r.get("id") or str(len(crm) + 1),
            "name": name,
            "sector": r.get("category") or r.get("sector") or "",
            "city": r.get("city") or "",
            "phone": r.get("phone") or "",
            "whatsapp": r.get("whatsapp") or "",
            "website": r.get("website") or "",
            "score": score,
            "status": "enviado",
            "last_update": day,
            "campaign": os.path.basename(campaign),
            "note": "Listo para envío (whatsapp_links.txt de la campaña)",
            "events": [{"date": day, "status": "enviado",
                        "note": f"Se importó de la campaña {os.path.basename(campaign)}"}],
        })
        added += 1
    _save(crm)
    print(f"seed: {added} nuevos, {updated} actualizados ({len(crm)} en total)")


def cmd_list(args) -> None:
    crm = _load()
    rows = crm
    if args.status:
        rows = [l for l in rows if l.get("status") == args.status]
    if not rows:
        print("No hay casos. Importa una campaña: python scripts/track.py seed --from out\\campaign_...")
        return
    for l in sorted(rows, key=lambda x: x.get("last_update") or "", reverse=True):
        due, action = _next_action(l)
        print(f"{l.get('id')} | {l.get('name'):<40} | {l.get('status'):<13} | "
              f"score {l.get('score')} | próx. {_fmt(due)} | {action}")


def cmd_today(args) -> None:
    crm = _load()
    day = _today()
    pending = [l for l in crm if l.get("status") not in CLOSED]
    due_list = []
    for l in pending:
        due, action = _next_action(l)
        if due <= day or l.get("status") == "respondio":
            due_list.append((l, due, action))
    if not due_list:
        print("Hoy no hay seguimientos pendientes. Revisa con: track.py list")
        return
    print(f"Seguimientos para hoy ({_fmt(day)}):\n")
    for l, due, action in sorted(due_list, key=lambda x: x[1]):
        print(f"[{l.get('id')}] {l.get('name')} — {action}")


def cmd_next(args) -> None:
    crm = _load()
    hits = _match(crm, args.key)
    if not hits:
        print(f"no encontré '{args.key}'. Usa: track.py list")
        return 1
    for l in hits[:5]:
        due, action = _next_action(l)
        print(f"\n{l.get('name')} (id {l.get('id')})")
        print(f"  estado:    {l.get('status')} — {STATUSES.get(l.get('status'), '')}")
        print(f"  whatsapp:  {l.get('whatsapp') or 'sin WhatsApp'}  | score: {l.get('score')}")
        print(f"  próxima:   {action}  (fecha límite {_fmt(due)})")
        print(f"  nota:      {l.get('note') or '-'}")


def cmd_update(args) -> None:
    crm = _load()
    hits = _match(crm, args.key)
    if not hits:
        print(f"no encontré '{args.key}'. Usa: track.py list")
        return 1
    l = hits[0]
    old = l.get("status")
    if args.status not in STATUSES:
        print(f"estado inválido '{args.status}'. Opciones: {', '.join(STATUSES)}", file=sys.stderr)
        return 1
    l["status"] = args.status
    l["last_update"] = _today()
    if args.note:
        l["note"] = args.note
    l.setdefault("events", []).append({
        "date": _today(),
        "status": args.status,
        "note": args.note or "",
    })
    _save(crm)
    due, action = _next_action(l)
    print(f"{l['name']}: {old} → {args.status}. Próxima acción: {action} (antes de {_fmt(due)}).")


def cmd_stats(args) -> None:
    crm = _load()
    if not crm:
        print("Sin datos.")
        return
    total = len(crm)
    print(f"Casos: {total}\n")
    print(f"{'Estado':<14} {'Cantidad':>8}")
    for s in STATUSES:
        n = sum(1 for l in crm if l.get("status") == s)
        if n:
            print(f"{s:<14} {n:>8}")
    socios = sum(1 for l in crm if l.get("status") == "socio")
    print("\n" + "─" * 26)
    print(f"Socios aliados: {socios} | Conversión: {socios/total*100:.0f}%")


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Seguimiento de casos de la campaña")
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("seed"); s.add_argument("--from", dest="from_dir", required=True)

    l = sub.add_parser("list"); l.add_argument("--status")

    sub.add_parser("today")

    n = sub.add_parser("next"); n.add_argument("key")

    u = sub.add_parser("update")
    u.add_argument("key")
    u.add_argument("--status", required=True)
    u.add_argument("--note", default="")

    sub.add_parser("stats")
    return p


def main() -> int:
    args = build_parser().parse_args()
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:
        pass
    fn = {"seed": cmd_seed, "list": cmd_list, "today": cmd_today,
          "next": cmd_next, "update": cmd_update, "stats": cmd_stats}[args.cmd]
    return fn(args) or 0


if __name__ == "__main__":
    raise SystemExit(main())
