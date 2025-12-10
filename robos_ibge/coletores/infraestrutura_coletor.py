"""Coletor de infraestrutura (saneamento, saúde, educação)."""
from __future__ import annotations

from typing import Any, Dict, List

from robos_ibge.api_clients.ibge_client import IbgeClient
from robos_ibge.coletores.base_coletor import BaseColetor
from robos_ibge.utils.logger import get_logger
from robos_ibge.utils.validadores import preparar_numero, validar_codigo_ibge

LOGGER = get_logger(__name__)


class InfraestruturaColetor(BaseColetor):
    """Implementa coleta combinada das tabelas 1384 e 5370 do SIDRA."""

    tipo = "infraestrutura"

    def __init__(self, teste: bool = False, anos: List[int] | None = None) -> None:
        super().__init__(teste=teste, anos=anos or [2010, 2022])
        self.client = IbgeClient()

    def coletar_para_municipio(self, municipio: Dict[str, Any]) -> List[Dict[str, Any]]:
        ibge_id = str(municipio["ibge_id"])
        if not validar_codigo_ibge(ibge_id):
            raise ValueError(f"Código IBGE inválido: {ibge_id}")

        registros: List[Dict[str, Any]] = []
        for ano in self.anos:
            saneamento = self.client.fetch_sidra("1384", "63,83,30335", str(ano))
            saude = self.client.fetch_sidra("5370", "10657,28450", str(ano))
            linha_base: Dict[str, Any] = {
                "inf_ibge_codigo": ibge_id,
                "inf_ano": int(ano),
                "inf_abastecimento_agua": None,
                "inf_esgotamento_sanitario": None,
                "inf_coleta_lixo": None,
                "inf_energia_eletrica": None,
                "inf_leitos_hospitalares": None,
                "inf_leitos_por_1000_hab": None,
                "inf_estabelecimentos_saude": None,
                "inf_medicos_por_1000_hab": None,
                "inf_escolas_fundamental": None,
                "inf_escolas_medio": None,
                "inf_escolas_superior": None,
                "inf_agencias_bancarias": None,
                "inf_correios": None,
                "inf_fonte": "IBGE SIDRA tabelas 1384 e 5370",
            }

            for linha in saneamento[1:]:
                if linha.get("Município") != ibge_id:
                    continue
                variavel = linha.get("D1C")
                if variavel == "63":
                    linha_base["inf_abastecimento_agua"] = preparar_numero(linha.get("V"))
                elif variavel == "83":
                    linha_base["inf_esgotamento_sanitario"] = preparar_numero(linha.get("V"))
                elif variavel == "30335":
                    linha_base["inf_coleta_lixo"] = preparar_numero(linha.get("V"))

            for linha in saude[1:]:
                if linha.get("Município") != ibge_id:
                    continue
                variavel = linha.get("D1C")
                if variavel == "10657":
                    linha_base["inf_estabelecimentos_saude"] = preparar_numero(linha.get("V"))
                elif variavel == "28450":
                    linha_base["inf_leitos_hospitalares"] = preparar_numero(linha.get("V"))

            registros.append(dict(linha_base))
        LOGGER.debug("Municipio %s: %d registros infraestrutura", ibge_id, len(registros))
        return registros
