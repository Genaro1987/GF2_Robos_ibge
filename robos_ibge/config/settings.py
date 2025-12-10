"""Configurações centralizadas do projeto."""
from __future__ import annotations

import os
from dataclasses import dataclass
from dotenv import load_dotenv


load_dotenv()


@dataclass
class Settings:
    """Representa as configurações principais carregadas do ambiente."""

    db_host: str = os.getenv("DB_HOST", "127.0.0.1")
    db_user: str = os.getenv("DB_USER", "root")
    db_password: str = os.getenv("DB_PASSWORD", "")
    db_name: str = os.getenv("DB_NAME", "cnpj_db")
    db_charset: str = os.getenv("DB_CHARSET", "utf8mb4")
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    ibge_timeout: int = int(os.getenv("IBGE_TIMEOUT", "30"))
    batch_size: int = int(os.getenv("BATCH_SIZE", "100"))

    def validate(self) -> None:
        """Valida as configurações essenciais e levanta exceção se algo estiver faltando."""

        missing = [
            key
            for key, value in self.__dict__.items()
            if value is None or (isinstance(value, str) and value == "")
        ]
        if missing:
            raise ValueError(f"Variáveis de ambiente obrigatórias faltando: {', '.join(missing)}")


settings = Settings()
