"""Classe base para coletores IBGE."""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, Iterable, List

from mysql.connector import MySQLConnection
from tqdm import tqdm

from robos_ibge.config.settings import settings
from robos_ibge.database.connection import connection_manager
from robos_ibge.database.queries import get_insert_query
from robos_ibge.utils.helpers import dividir_em_lotes
from robos_ibge.utils.logger import get_logger
from robos_ibge.utils.validadores import validar_ano

LOGGER = get_logger(__name__, level=settings.log_level)


class BaseColetor(ABC):
    """Define funcionalidades comuns aos coletores."""

    tipo: str

    def __init__(self, teste: bool = False, anos: Iterable[int] | None = None) -> None:
        self.teste = teste
        self.anos = list(anos) if anos else []
        self.batch_size = settings.batch_size
        self.erros: List[str] = []

    def obter_municipios(self) -> List[Dict[str, Any]]:
        """Carrega a lista de municípios da tabela dim_ibge_municipios."""

        query = "SELECT ibge_id, nome, uf_sigla FROM dim_ibge_municipios ORDER BY ibge_id"
        conn = connection_manager.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query)
        resultados = cursor.fetchall()
        cursor.close()
        conn.close()
        if self.teste:
            resultados = resultados[:10]
        return resultados

    def _validar_contexto(self) -> None:
        """Valida anos e demais pré-condições."""

        for ano in self.anos:
            if not validar_ano(int(ano), 1900, 2100):
                raise ValueError(f"Ano inválido informado: {ano}")

    @abstractmethod
    def coletar_para_municipio(self, municipio: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Realiza a coleta para um único município."""

    def salvar_lote(self, conn: MySQLConnection, registros: List[Dict[str, Any]]) -> None:
        """Efetua inserções em lote com UPSERT."""

        query = get_insert_query(self.tipo)
        cursor = conn.cursor()
        cursor.executemany(query, registros)
        conn.commit()
        cursor.close()

    def processar(self) -> None:
        """Executa a coleta completa para todos os municípios e anos configurados."""

        self._validar_contexto()
        municipios = self.obter_municipios()
        LOGGER.info("Iniciando coleta %s para %d municípios", self.tipo, len(municipios))
        progresso = tqdm(municipios, desc=f"Coleta {self.tipo}", unit="município")
        conn = connection_manager.get_connection()
        try:
            for municipio in progresso:
                try:
                    registros = self.coletar_para_municipio(municipio)
                    for lote in dividir_em_lotes(registros, self.batch_size):
                        if lote:
                            self.salvar_lote(conn, lote)
                except Exception as exc:  # noqa: BLE001
                    msg = f"Falha em {municipio.get('ibge_id')}: {exc}"
                    LOGGER.error(msg)
                    self.erros.append(msg)
            LOGGER.info("Coleta %s finalizada com %d erros", self.tipo, len(self.erros))
        finally:
            conn.close()
