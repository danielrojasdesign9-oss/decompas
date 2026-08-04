"""Modelo de datos y utilidades de normalización para leads de Pymes."""
from __future__ import annotations

import re
import uuid
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class Lead:
    """Lead normalizado de una Pyme local."""

    name: str = ""
    source: str = ""
    category: str = ""
    address: str = ""
    city: str = ""
    website: str = ""
    phone: str = ""
    whatsapp: str = ""
    whatsapp_url: str = ""
    google_rating: float | None = None
    google_reviews: int | None = None
    social: dict = field(default_factory=dict)
    notes: str = ""
    raw: dict = field(default_factory=dict)
    captured_at: str = ""

    def __post_init__(self) -> None:
        if not self.captured_at:
            self.captured_at = _now_iso()
        if not getattr(self, "id", ""):
            self.id = uuid.uuid4().hex[:12]

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_raw(cls, **kwargs) -> "Lead":
        return cls(**kwargs)


def clean_phone(raw: str | None) -> str:
    """Limpia un teléfono dejando solo dígitos (mantiene + inicial opcional)."""
    if not raw:
        return ""
    raw = raw.strip().replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
    return raw


def to_international(digits: str, default_country: str = "57") -> str:
    """Convierte dígitos locales a número internacional (E.164 sin '+').

    Reglas Colombia (default_country="57"):
      - Móvil 3XXXXXXXXX        -> +573XXXXXXXXX
      - Fijo 60X XXXXXXX        -> +57X XXXXXXX (se descarta el "60")
      - Ya internacional (57+..) se respeta.
    """
    if not digits:
        return ""
    if digits.startswith("00"):
        digits = digits[2:]
    digits = digits.lstrip("+")
    cc = (default_country or "").strip("+")
    if cc and digits.startswith(cc) and len(digits) >= len(cc) + 8:
        return digits
    if len(digits) == 10:
        if cc == "57":
            if digits.startswith("3"):
                return cc + digits
            if digits.startswith("60"):
                return cc + digits[2:]
        return cc + digits if cc else digits
    return digits


def _whatsapp_compatible(number: str) -> bool:
    """Solo números que pueden recibir WhatsApp (Colombia: móviles 573...)."""
    if not number:
        return False
    if number.startswith("57") and len(number) == 12:
        return number.startswith("573")
    return True


def build_whatsapp_url(number: str) -> str:
    digits = re.sub(r"[^\d]", "", number)
    if not digits:
        return ""
    return f"https://wa.me/{digits}"


def normalize_lead(lead: Lead, default_country: str = "57") -> Lead:
    """Normaliza campos clave (website, teléfono, WhatsApp) de un lead."""
    lead.website = (lead.website or "").strip().rstrip("/")
    wa = to_international(clean_phone(lead.whatsapp or lead.phone), default_country)
    lead.whatsapp = wa if _whatsapp_compatible(wa) else ""
    lead.whatsapp_url = build_whatsapp_url(lead.whatsapp)
    return lead
