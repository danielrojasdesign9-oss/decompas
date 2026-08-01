"""Fuente directorios: crawler genérico configurable para directorios
locales, cámaras de comercio y listados sectoriales.

Configuración JSON de ejemplo:
{
  "urls": ["https://example.com/directorio?pagina={page}"],
  "pagination": {"max_pages": 3},
  "selectors": {
    "item": "div.card",
    "name": "h2",
    "website": "a.website",
    "phone": ".phone",
    "address": ".address"
  }
}
"""
from __future__ import annotations

import json
from typing import Iterable
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from ..models import Lead, normalize_lead
from .base import BaseSource


class DirectorySource(BaseSource):
    name = "directories"

    def __init__(self, config_path: str, default_country: str = "52",
                 timeout: int = 30, headers: dict | None = None):
        with open(config_path, encoding="utf-8") as f:
            self.config = json.load(f)
        self.default_country = default_country
        self.timeout = timeout
        self.headers = headers or {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) DeCompas-LeadEngine/1.0"
        }

    def fetch(self, **kwargs) -> Iterable[Lead]:
        selectors = self.config.get("selectors", {})
        max_pages = self.config.get("pagination", {}).get("max_pages", 1)
        seen: set[str] = set()
        for url in self.config.get("urls", []):
            for page in range(1, max_pages + 1):
                target = url.format(page=page)
                try:
                    resp = requests.get(target, headers=self.headers, timeout=self.timeout)
                    resp.raise_for_status()
                except requests.RequestException as e:
                    print(f"  [directories] error {target}: {e}")
                    continue
                soup = BeautifulSoup(resp.text, "html.parser")
                items = soup.select(selectors.get("item", "article"))
                if not items:
                    break
                for el in items:
                    lead = self._extract_item(el, selectors)
                    if not lead or not lead.name or lead.name in seen:
                        continue
                    seen.add(lead.name)
                    yield normalize_lead(lead, self.default_country)

    def _extract_item(self, el, s: dict) -> Lead | None:
        name = self._text(el, s.get("name")) or self._text(el, s.get("item"))
        if not name:
            return None
        website = self._href(el, s.get("website")) or ""
        lead = Lead(
            name=name,
            source=self.name,
            website=website,
            phone=self._text(el, s.get("phone")),
            address=self._text(el, s.get("address")),
            category=self._text(el, s.get("category")),
        )
        return lead

    @staticmethod
    def _text(el, selector: str | None) -> str:
        if not selector:
            return ""
        node = el.select_one(selector)
        return (node.get_text(strip=True) if node else "")

    @staticmethod
    def _href(el, selector: str | None) -> str:
        if not selector:
            return ""
        node = el.select_one(selector)
        return (node.get("href") or "") if node else ""
