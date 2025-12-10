"""Cliente para consumo dos dados do Atlas Brasil ou CSV manual."""
from __future__ import annotations

import csv
from pathlib import Path
from typing import Dict, Iterable, List

from robos_ibge.utils.logger import get_logger

LOGGER = get_logger(__name__)


class AtlasBrasilClient:
    """Cliente simplificado preparado para API futura ou CSV local."""

    def __init__(self, csv_path: str | None = None) -> None:
        self.csv_path = Path(csv_path) if csv_path else None

    def load_from_csv(self) -> List[Dict[str, str]]:
        """Carrega dados de um CSV exportado do Atlas Brasil."""

        if not self.csv_path or not self.csv_path.exists():
            raise FileNotFoundError("Caminho CSV do Atlas Brasil não configurado ou inexistente.")

        LOGGER.info("Carregando dados do Atlas Brasil via CSV: %s", self.csv_path)
        with self.csv_path.open("r", encoding="utf-8") as handle:
            reader: Iterable[Dict[str, str]] = csv.DictReader(handle)
            return [dict(row) for row in reader]
