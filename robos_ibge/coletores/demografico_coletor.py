"""Coletor de dados demográficos (população)."""
from __future__ import annotations

from typing import Any, Dict, List

from robos_ibge.api_clients.ibge_client import IbgeClient
from robos_ibge.coletores.base_coletor import BaseColetor
from robos_ibge.utils.logger import get_logger
from robos_ibge.utils.validadores import preparar_numero, validar_codigo_ibge

LOGGER = get_logger(__name__)


class DemograficoColetor(BaseColetor):
    """Implementação de coleta populacional via SIDRA (tabela 6579)."""

    tipo = "demografico"

    def __init__(self, teste: bool = False, anos: List[int] | None = None) -> None:
        super().__init__(teste=teste, anos=anos or [2010, 2022, 2023, 2024])
        self.client = IbgeClient()

    def coletar_para_municipio(self, municipio: Dict[str, Any]) -> List[Dict[str, Any]]:
        ibge_id = str(municipio["ibge_id"])
        if not validar_codigo_ibge(ibge_id):
            raise ValueError(f"Código IBGE inválido: {ibge_id}")

        registros: List[Dict[str, Any]] = []
        for ano in self.anos:
            dados = self.client.fetch_sidra("6579", "9324", str(ano))
            # Resposta contém cabeçalho na primeira posição
            for linha in dados[1:]:
                if linha.get("Município") != ibge_id:
                    continue
                registros.append(
                    {
                        "dem_ibge_codigo": ibge_id,
                        "dem_ano": int(ano),
                        "dem_pop_total": preparar_numero(linha.get("V")),
                        "dem_pop_urbana": None,
                        "dem_pop_rural": None,
                        "dem_pop_homens": None,
                        "dem_pop_mulheres": None,
                        "dem_densidade_demografica": None,
                        "dem_pop_0_14": None,
                        "dem_pop_15_64": None,
                        "dem_pop_65_mais": None,
                        "dem_taxa_crescimento": None,
                        "dem_fonte": "IBGE SIDRA tabela 6579",
                    }
                )
        LOGGER.debug("Municipio %s: %d registros demográficos", ibge_id, len(registros))
        return registros
