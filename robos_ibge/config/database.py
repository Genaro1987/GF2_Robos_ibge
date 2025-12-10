"""Configurações relacionadas ao banco de dados MySQL."""
from __future__ import annotations

from typing import Dict, Any

from robos_ibge.config.settings import settings


def database_config() -> Dict[str, Any]:
    """Retorna o dicionário de configuração do MySQL Connector."""

    return {
        "host": settings.db_host,
        "user": settings.db_user,
        "password": settings.db_password,
        "database": settings.db_name,
        "charset": settings.db_charset,
        "auth_plugin": "mysql_native_password",
    }


def connection_uri() -> str:
    """Gera uma URI textual útil para logs."""

    return f"mysql://{settings.db_user}@{settings.db_host}/{settings.db_name}"
