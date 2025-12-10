"""Cliente para consumir APIs do IBGE."""
from __future__ import annotations

from typing import Any, Dict, List, Optional

import requests
from retry import retry

from robos_ibge.config.settings import settings
from robos_ibge.utils.logger import get_logger

LOGGER = get_logger(__name__)


class IbgeClient:
    """Cliente HTTP para consultas ao SIDRA e Agregados."""

    SIDRA_BASE = "https://apisidra.ibge.gov.br/values"
    AGREGADOS_BASE = "https://servicodados.ibge.gov.br/api/v3/agregados"

    def __init__(self, timeout: Optional[int] = None) -> None:
        self.timeout = timeout or settings.ibge_timeout

    @retry(tries=3, delay=2, backoff=2, logger=LOGGER)
    def fetch_sidra(self, tabela: str, variaveis: str, ano: str) -> List[Dict[str, Any]]:
        """Consulta a API SIDRA com retentativas."""

        url = f"{self.SIDRA_BASE}/t/{tabela}/n6/all/v/{variaveis}/p/{ano}"
        LOGGER.debug("Requisitando SIDRA: %s", url)
        resp = requests.get(url, timeout=self.timeout)
        resp.raise_for_status()
        data = resp.json()
        if not isinstance(data, list):
            raise ValueError("Resposta inesperada da API SIDRA")
        return data

    @retry(tries=3, delay=2, backoff=2, logger=LOGGER)
    def fetch_agregado(self, agregado_id: str, ano: str, variaveis: str) -> List[Dict[str, Any]]:
        """Consulta a API de agregados do IBGE."""

        url = f"{self.AGREGADOS_BASE}/{agregado_id}/periodos/{ano}/variaveis/{variaveis}"
        LOGGER.debug("Requisitando Agregados: %s", url)
        resp = requests.get(url, timeout=self.timeout)
        resp.raise_for_status()
        data = resp.json()
        if not isinstance(data, list):
            raise ValueError("Resposta inesperada da API de agregados")
        return data
