"""Script de setup inicial para preparação do ambiente."""
from __future__ import annotations

import os
from pathlib import Path
from typing import List

import mysql.connector

from robos_ibge.config.settings import settings
from robos_ibge.database.connection import connection_manager
from robos_ibge.utils.logger import get_logger

LOGGER = get_logger(__name__, level=settings.log_level)
BASE_DIR = Path(__file__).parent


def validar_env() -> None:
    """Valida variáveis essenciais do .env."""

    settings.validate()
    LOGGER.info("Variáveis de ambiente validadas com sucesso")


def executar_migrations() -> None:
    """Executa o arquivo migrations.sql para criar tabelas."""

    caminho_sql = BASE_DIR / "database" / "migrations.sql"
    sql_texto = caminho_sql.read_text(encoding="utf-8")
    conn = connection_manager.get_connection()
    cursor = conn.cursor()
    for statement in sql_texto.split(";"):
        stmt = statement.strip()
        if not stmt:
            continue
        cursor.execute(stmt)
    conn.commit()
    cursor.close()
    conn.close()
    LOGGER.info("Tabelas verificadas/criadas com sucesso")


def verificar_municipios() -> None:
    """Confere se a tabela dim_ibge_municipios possui dados."""

    conn = connection_manager.get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(1) FROM dim_ibge_municipios")
    total = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    if total == 0:
        LOGGER.warning("Tabela dim_ibge_municipios está vazia. Popule-a antes das coletas.")
    else:
        LOGGER.info("dim_ibge_municipios possui %d registros", total)


def criar_pastas() -> None:
    """Garante a existência das pastas de logs e cache."""

    for pasta in [BASE_DIR / "logs", BASE_DIR / "data"]:
        os.makedirs(pasta, exist_ok=True)
    LOGGER.info("Pastas de trabalho conferidas")


def testar_conexao() -> None:
    """Realiza um teste rápido de conexão ao banco."""

    if not connection_manager.test_connection():
        raise mysql.connector.Error("Não foi possível conectar ao banco com as credenciais fornecidas")


if __name__ == "__main__":
    validar_env()
    criar_pastas()
    testar_conexao()
    executar_migrations()
    verificar_municipios()
    LOGGER.info("Setup concluído")
