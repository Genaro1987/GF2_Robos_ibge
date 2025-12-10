"""Coletor de PIB municipal."""
from __future__ import annotations

from typing import Any, Dict, List

from robos_ibge.api_clients.ibge_client import IbgeClient
from robos_ibge.coletores.base_coletor import BaseColetor
from robos_ibge.utils.logger import get_logger
from robos_ibge.utils.validadores import preparar_numero, validar_codigo_ibge

LOGGER = get_logger(__name__)


class PibColetor(BaseColetor):
    """Coleta dados de PIB pela tabela 5938 do SIDRA."""

    tipo = "pib"

    def __init__(self, teste: bool = False, anos: List[int] | None = None) -> None:
        super().__init__(teste=teste, anos=anos or [2010, 2015, 2019, 2020, 2021])
        self.client = IbgeClient()

    def coletar_para_municipio(self, municipio: Dict[str, Any]) -> List[Dict[str, Any]]:
        ibge_id = str(municipio["ibge_id"])
        if not validar_codigo_ibge(ibge_id):
            raise ValueError(f"Código IBGE inválido: {ibge_id}")

        registros: List[Dict[str, Any]] = []
        variaveis = "37,517,513,514,515,516,518"
        for ano in self.anos:
            dados = self.client.fetch_sidra("5938", variaveis, str(ano))
            for linha in dados[1:]:
                if linha.get("Município") != ibge_id:
                    continue
                registros.append(
                    {
                        "pib_ibge_codigo": ibge_id,
                        "pib_ano": int(ano),
                        "pib_total": preparar_numero(linha.get("V")) if linha.get("D1C") == "37" else None,
                        "pib_per_capita": preparar_numero(linha.get("V")) if linha.get("D1C") == "517" else None,
                        "pib_agropecuaria": preparar_numero(linha.get("V")) if linha.get("D1C") == "513" else None,
                        "pib_industria": preparar_numero(linha.get("V")) if linha.get("D1C") == "514" else None,
                        "pib_servicos": preparar_numero(linha.get("V")) if linha.get("D1C") == "515" else None,
                        "pib_administracao_publica": preparar_numero(linha.get("V")) if linha.get("D1C") == "516" else None,
                        "pib_impostos": preparar_numero(linha.get("V")) if linha.get("D1C") == "518" else None,
                        "pib_va_total": None,
                        "pib_fonte": "IBGE SIDRA tabela 5938",
                    }
                )
        LOGGER.debug("Municipio %s: %d registros PIB", ibge_id, len(registros))
        return registros
