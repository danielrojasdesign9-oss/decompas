"""Clase base para fuentes de extracción de leads."""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Iterable

from ..models import Lead


class BaseSource(ABC):
    """Contrato común para toda fuente de leads (Google Maps, directorios, demo)."""

    name: str = "base"

    @abstractmethod
    def fetch(self, **kwargs) -> Iterable[Lead]:
        """Extrae un iterable de leads normalizados."""
        raise NotImplementedError
