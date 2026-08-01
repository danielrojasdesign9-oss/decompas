"""Fuente Google Maps: Places API (Nueva) con fallback de scraping.

Usa la Places API nueva de Google (`places:v1`), que requiere una API key
con Places API habilitada. La key se lee de la variable de entorno
`GOOGLE_MAPS_API_KEY` o del argumento `api_key`.
"""
from __future__ import annotations

import json
import time
from typing import Iterable

import requests

from ..models import Lead, normalize_lead
from .base import BaseSource

PLACES_SEARCH_URL = "https://places.googleapis.com/v1/places:searchText"

DEFAULT_FIELDS = [
    "places.displayName",
    "places.formattedAddress",
    "places.nationalPhoneNumber",
    "places.internationalPhoneNumber",
    "places.websiteUri",
    "places.rating",
    "places.userRatingCount",
    "places.types",
    "places.primaryTypeDisplayName",
    "places.googleMapsUri",
    "places.editorialSummary",
    "places.location",
]


class GoogleMapsSource(BaseSource):
    name = "google_maps"

    def __init__(
        self,
        api_key: str,
        default_country: str = "52",
        fields: list[str] | None = None,
        timeout: int = 30,
    ):
        self.api_key = api_key
        self.default_country = default_country
        self.fields = fields or DEFAULT_FIELDS
        self.timeout = timeout

    # ------------------------------------------------------------------ API
    def fetch(self, query: str, city: str = "", max_results: int = 50,
              region: str | None = None) -> Iterable[Lead]:
        """Busca negocios con texto libre.

        Args:
            query: tipo de negocio (ej. "restaurantes", "clínicas dentales").
            city: ciudad/colonia para acotar la búsqueda.
            max_results: máximo de resultados a recolectar.
            region: "lat,lng,radius_m" para acotar con círculo.
        """
        text_query = f"{query} in {city}" if city else query
        headers = {
            "Content-Type": "application/json",
            "X-Goog-Api-Key": self.api_key,
            "X-Goog-FieldMask": ",".join(self.fields),
        }
        payload: dict = {"textQuery": text_query, "pageSize": min(max_results, 20)}
        if region:
            lat, lng, radius = region.split(",")
            payload["locationRestriction"] = {
                "circle": {"center": {"latitude": float(lat), "longitude": float(lng)},
                           "radius": float(radius)}
            }

        collected = 0
        page_token: str | None = None
        while collected < max_results:
            if page_token:
                payload = {"textQuery": text_query, "pageSize": min(max_results, 20), "pageToken": page_token}
            resp = requests.post(PLACES_SEARCH_URL, headers=headers, json=payload, timeout=self.timeout)
            if resp.status_code != 200:
                raise RuntimeError(f"Places API error {resp.status_code}: {resp.text[:400]}")
            data = resp.json()
            for place in data.get("places", []):
                lead = self._place_to_lead(place, city)
                yield lead
                collected += 1
                if collected >= max_results:
                    break
            page_token = data.get("nextPageToken")
            if not page_token:
                break
            time.sleep(2)  # respeta el tiempo de los tokens de paginación

    def _place_to_lead(self, place: dict, city: str) -> Lead:
        display = (place.get("displayName") or {}).get("text", "")
        phone = place.get("nationalPhoneNumber") or place.get("internationalPhoneNumber") or ""
        lead = Lead(
            name=display,
            source=self.name,
            category=(place.get("primaryTypeDisplayName") or {}).get("text", ""),
            address=place.get("formattedAddress", ""),
            city=city,
            website=place.get("websiteUri", ""),
            phone=phone,
            google_rating=place.get("rating"),
            google_reviews=place.get("userRatingCount"),
            notes=(place.get("editorialSummary") or {}).get("text", ""),
            raw=place,
        )
        return normalize_lead(lead, self.default_country)

    # ----------------------------------------------------------- scraping
    def fetch_scraped(self, query: str, city: str = "", max_results: int = 30,
                      headless: bool = True) -> Iterable[Lead]:
        """Variante con Playwright sobre maps.google.com (sin API key).

        Es más frágil y sujeta a cambios del DOM; se ofrece como respaldo.
        Requiere: `pip install playwright && playwright install chromium`.
        """
        try:
            from playwright.sync_api import sync_playwright
        except ImportError:
            raise RuntimeError("Playwright no está instalado. Ejecuta: pip install playwright && playwright install chromium")

        url = f"https://www.google.com/maps/search/{query}+{city}".replace(" ", "+")
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=headless)
            page = browser.new_page()
            page.goto(url, timeout=60000)
            page.wait_for_timeout(3000)
            for _ in range(max_results // 10):
                page.mouse.wheel(0, 6000)
                page.wait_for_timeout(1500)
            items = page.locator('a[aria-label*=","]').evaluate_all(
                "els => els.map(e => ({name: e.getAttribute('aria-label'), href: e.href}))"
            )
            browser.close()

        seen: set[str] = set()
        for item in items[:max_results]:
            name = (item.get("name") or "").split(",")[0]
            if not name or name in seen:
                continue
            seen.add(name)
            lead = Lead(name=name, source=self.name, city=city, raw=item)
            yield normalize_lead(lead, self.default_country)


def load_from_env() -> str:
    """Lee la API key desde el entorno o un archivo .env en cwd."""
    import os
    key = os.environ.get("GOOGLE_MAPS_API_KEY", "")
    if not key and os.path.exists(".env"):
        with open(".env", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line.startswith("GOOGLE_MAPS_API_KEY="):
                    key = line.split("=", 1)[1].strip().strip('"').strip("'")
                    break
    return key


def _json_dumps(obj):
    return json.dumps(obj, ensure_ascii=False, indent=2)
