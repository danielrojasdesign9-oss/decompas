"""Exportación de leads a JSON y CSV."""
from __future__ import annotations

import csv
import json
import os
from datetime import datetime

from .models import Lead

CSV_COLUMNS = [
    "id", "name", "source", "category", "address", "city", "website",
    "phone", "whatsapp", "whatsapp_url", "google_rating", "google_reviews",
    "facebook", "instagram", "tiktok", "x", "linkedin", "captured_at",
]


def _csv_row(lead: Lead) -> list:
    social = lead.social or {}
    return [
        lead.id, lead.name, lead.source, lead.category, lead.address, lead.city,
        lead.website, lead.phone, lead.whatsapp, lead.whatsapp_url,
        lead.google_rating or "", lead.google_reviews or "",
        social.get("facebook", ""), social.get("instagram", ""),
        social.get("tiktok", ""), social.get("x", ""), social.get("linkedin", ""),
        lead.captured_at,
    ]


def export_json(leads: list[Lead], out_dir: str = "data", filename: str | None = None) -> str:
    os.makedirs(out_dir, exist_ok=True)
    name = filename or f"leads_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    path = os.path.join(out_dir, name)
    with open(path, "w", encoding="utf-8") as f:
        json.dump([l.to_dict() for l in leads], f, ensure_ascii=False, indent=2)
    return path


def export_csv(leads: list[Lead], out_dir: str = "data", filename: str | None = None) -> str:
    os.makedirs(out_dir, exist_ok=True)
    name = filename or f"leads_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    path = os.path.join(out_dir, name)
    with open(path, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(CSV_COLUMNS)
        for lead in leads:
            writer.writerow(_csv_row(lead))
    return path
