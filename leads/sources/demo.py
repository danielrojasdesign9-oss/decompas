"""Fuente demo: genera leads de ejemplo para probar el pipeline sin API keys."""
from __future__ import annotations

from typing import Iterable

from ..models import Lead, normalize_lead
from .base import BaseSource

SAMPLE = [
    dict(name="Taquería El Buen Sabor", category="Restaurante", city="Monterrey",
         website="https://elbuensabor.example", phone="+52 81 1234 5678",
         google_rating=4.6, google_reviews=320, address="Av. Juárez 120, Centro"),
    dict(name="Clínica Dental Sonrisa", category="Clínica dental", city="Monterrey",
         website="", phone="+52 81 8765 4321",
         google_rating=4.9, google_reviews=88, address="Col. Roma, Monterrey"),
    dict(name="DulceMomento Pastelería", category="Pastelería", city="Monterrey",
         website="https://dulcemomento.example", phone="8123456789",
         google_rating=4.3, google_reviews=45, address="San Pedro"),
]


class DemoSampleSource(BaseSource):
    name = "demo"

    def __init__(self, default_country: str = "52"):
        self.default_country = default_country

    def fetch(self, **kwargs) -> Iterable[Lead]:
        for row in SAMPLE:
            yield normalize_lead(Lead(**row, source=self.name), self.default_country)
