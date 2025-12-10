"""Gerenciador de conexões com MySQL."""
from __future__ import annotations

import mysql.connector
from mysql.connector import pooling, MySQLConnection
from typing import Optional

from robos_ibge.config.database import database_config
from robos_ibge.utils.logger import get_logger

LOGGER = get_logger(__name__)


class ConnectionManager:
    """Pool de conexões para reutilização eficiente."""

    def __init__(self, pool_name: str = "ibge_pool", pool_size: int = 5) -> None:
        self._pool: Optional[pooling.MySQLConnectionPool] = None
        self.pool_name = pool_name
        self.pool_size = pool_size

    def init_pool(self) -> None:
        """Inicializa o pool se ainda não existir."""

        if self._pool:
            return
        config = database_config()
        self._pool = pooling.MySQLConnectionPool(
            pool_name=self.pool_name,
            pool_size=self.pool_size,
            **config,
        )
        LOGGER.debug("Pool de conexões '%s' inicializado", self.pool_name)

    def get_connection(self) -> MySQLConnection:
        """Obtém uma conexão do pool."""

        if not self._pool:
            self.init_pool()
        assert self._pool is not None
        return self._pool.get_connection()

    def test_connection(self) -> bool:
        """Testa a conexão básica com o banco de dados."""

        try:
            conn = mysql.connector.connect(**database_config())
            conn.close()
            LOGGER.info("Conexão com o banco de dados bem-sucedida")
            return True
        except mysql.connector.Error as exc:
            LOGGER.error("Falha ao conectar no banco: %s", exc)
            return False


def get_connection() -> MySQLConnection:
    """Retorna uma conexão única (fora do pool) para operações isoladas."""

    return mysql.connector.connect(**database_config())


connection_manager = ConnectionManager()
