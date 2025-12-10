"""Coletor de índices socioeconômicos (IDH)."""
from __future__ import annotations

from typing import Any, Dict, List

from robos_ibge.api_clients.atlas_brasil_client import AtlasBrasilClient
from robos_ibge.coletores.base_coletor import BaseColetor
from robos_ibge.utils.logger import get_logger
from robos_ibge.utils.validadores import preparar_numero, validar_codigo_ibge

LOGGER = get_logger(__name__)


class SocioeconomicoColetor(BaseColetor):
    """Carrega dados do Atlas Brasil ou CSV manual."""

    tipo = "socioeconomico"

    def __init__(self, teste: bool = False, anos: List[int] | None = None, csv_path: str | None = None) -> None:
        super().__init__(teste=teste, anos=anos or [2010, 2021])
        self.client = AtlasBrasilClient(csv_path=csv_path)

    def coletar_para_municipio(self, municipio: Dict[str, Any]) -> List[Dict[str, Any]]:
        ibge_id = str(municipio["ibge_id"])
        if not validar_codigo_ibge(ibge_id):
            raise ValueError(f"Código IBGE inválido: {ibge_id}")

        try:
            dados = self.client.load_from_csv()
        except FileNotFoundError:
            LOGGER.warning("CSV do Atlas Brasil não encontrado. Nenhum dado será importado para %s", ibge_id)
            return []

        registros: List[Dict[str, Any]] = []
        for linha in dados:
            if linha.get("Codmun7") != ibge_id or int(linha.get("Ano", 0)) not in self.anos:
                continue
            registros.append(
                {
                    "idx_ibge_codigo": ibge_id,
                    "idx_ano": int(linha["Ano"]),
                    "idx_idhm": preparar_numero(linha.get("IDHM")),
                    "idx_idhm_renda": preparar_numero(linha.get("IDHM_Renda")),
                    "idx_idhm_longevidade": preparar_numero(linha.get("IDHM_Longevidade")),
                    "idx_idhm_educacao": preparar_numero(linha.get("IDHM_Educacao")),
                    "idx_renda_per_capita": preparar_numero(linha.get("Renda_pc")),
                    "idx_gini": preparar_numero(linha.get("Gini")),
                    "idx_percentual_pobres": preparar_numero(linha.get("Pobres")),
                    "idx_percentual_extrema_pobreza": preparar_numero(linha.get("ExtremaPobreza")),
                    "idx_taxa_alfabetizacao": preparar_numero(linha.get("Taxa_Alfabetizacao")),
                    "idx_anos_estudo_medio": preparar_numero(linha.get("Anos_Estud")),
                    "idx_frequencia_escolar_6_14": preparar_numero(linha.get("Freq_Escolar")),
                    "idx_taxa_desemprego": preparar_numero(linha.get("Desemprego")),
                    "idx_taxa_formalizacao": preparar_numero(linha.get("Formalizacao")),
                    "idx_esperanca_vida": preparar_numero(linha.get("Esperanca_Vida")),
                    "idx_mortalidade_infantil": preparar_numero(linha.get("Mort_Infantil")),
                    "idx_fonte": "Atlas Brasil (CSV)",
                }
            )
        LOGGER.debug("Municipio %s: %d registros socioeconômicos", ibge_id, len(registros))
        return registros
