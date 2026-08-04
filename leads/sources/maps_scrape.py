"""Fuente Google Maps por scraping (respaldo sin API key).

Abre cada negocio en maps.google.com y extrae nombre, teléfono, web, rating
y dirección con Playwright. Es más frágil que la Places API: si Google cambia
el DOM o bloquea la sesión, puede fallar. Se usa como respaldo automático.

Requiere: `pip install playwright && playwright install chromium`
"""
from __future__ import annotations

import re
import time
from typing import Iterable

from ..models import Lead, normalize_lead
from .base import BaseSource

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36"
)
PHONE_BTN = 'button[data-item-id*="phone:tel:"]'
WEBSITE_A = 'a[data-item-id*="authority"], a[href^="http"][data-tooltip*="eite"]'

RATING_RE = re.compile(r"([\d.,]+)\s*★")
REVIEWS_RE = re.compile(r"\(([\d.,]+)\)")


class MapsScrapeSource(BaseSource):
    name = "maps_scrape"

    def __init__(self, default_country: str = "57", headless: bool = True,
                 timeout_ms: int = 5000):
        self.default_country = default_country
        self.headless = headless
        self.timeout_ms = timeout_ms

    def fetch(self, query: str = "", city: str = "", max_results: int = 30,
              max_per_sector: int = 10, **kwargs) -> Iterable[Lead]:
        try:
            from playwright.sync_api import sync_playwright
        except ImportError:
            raise RuntimeError("Playwright no está instalado. Ejecuta: "
                               "pip install playwright && playwright install chromium")

        term = f"{query} {city}".strip().replace(" ", "+")
        url = f"https://www.google.com/maps/search/{term}"

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=self.headless)
            page = browser.new_page(user_agent=USER_AGENT,
                                    viewport={"width": 1366, "height": 900},
                                    locale="es-CO")
            page.goto(url, timeout=60000)
            page.wait_for_timeout(3500)
            self._dismiss_consent(page)

            anchors = self._collect_anchors(page, max_results)
            count = 0
            for anchor in anchors[:max_results]:
                try:
                    lead = self._extract_place(page, anchor, city)
                except Exception:
                    continue
                if not lead or not lead.name:
                    continue
                yield normalize_lead(lead, self.default_country)
                count += 1
                if count >= max_results:
                    break
            browser.close()

    @staticmethod
    def _dismiss_consent(page) -> None:
        for text in ("Rechazar todo", "Accept all", "Rechazo todo", "Acepto todo"):
            try:
                btn = page.locator(f'button:has-text("{text}")').first
                if btn.count() and btn.is_visible():
                    btn.click(timeout=3000)
                    page.wait_for_timeout(800)
                    return
            except Exception:
                pass

    def _collect_anchors(self, page, max_results: int) -> list:
        for _ in range((max_results // 8) + 1):
            page.mouse.wheel(0, 4000)
            page.wait_for_timeout(900)
        feed = page.locator('div[role="feed"] a[href^="https://www.google.com/maps/place/"]')
        anchors = feed.all()
        seen, out = set(), []
        for a in anchors:
            href = a.get_attribute("href") or ""
            if href not in seen:
                seen.add(href)
                out.append(a)
        return out

    def _extract_place(self, page, anchor, city: str) -> Lead | None:
        label = anchor.get_attribute("aria-label") or anchor.inner_text()
        name = label.split(",")[0].strip()
        if not name:
            return None

        rating = self._num(RATING_RE.search(label))
        reviews = self._int(REVIEWS_RE.search(label))
        address = ""
        m = re.search(r"·\s*(.*)$", label)
        if m:
            address = m.group(1).strip()

        phone, website = "", ""
        try:
            anchor.click(timeout=self.timeout_ms)
            page.wait_for_timeout(1400)
            phone = self._extract_phone(page)
            website = self._extract_website(page)
        except Exception:
            pass
        finally:
            try:
                page.keyboard.press("Escape")
            except Exception:
                pass

        return Lead(name=name, source=self.name, category="", address=address,
                    city=city, website=website, phone=phone,
                    google_rating=rating, google_reviews=reviews)

    def _extract_phone(self, page) -> str:
        try:
            btn = page.locator(PHONE_BTN).first
            if btn.count() == 0:
                return ""
            text = (btn.text_content(timeout=3000) or "").strip()
            if text:
                return text
            attrs = (btn.get_attribute("data-item-id") or "")
            m = re.search(r"tel:([+\d\s\-]+)", attrs)
            if m:
                return m.group(1).strip()
        except Exception:
            pass
        return ""

    def _extract_website(self, page) -> str:
        try:
            a = page.locator(WEBSITE_A).first
            if a.count() == 0:
                return ""
            href = (a.get_attribute("href") or "").strip()
            if href.startswith("http"):
                return href
        except Exception:
            pass
        return ""

    @staticmethod
    def _num(match) -> float | None:
        if not match:
            return None
        try:
            return float(match.group(1).replace(",", "."))
        except ValueError:
            return None

    @staticmethod
    def _int(match) -> int | None:
        if not match:
            return None
        try:
            return int(re.sub(r"[^\d]", "", match.group(1)))
        except ValueError:
            return None
