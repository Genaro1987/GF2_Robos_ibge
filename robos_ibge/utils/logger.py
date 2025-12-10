"""Utilitário de logging com cores e rotação diária."""
from __future__ import annotations

import logging
import os
from datetime import datetime
from typing import Optional

LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")

if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR, exist_ok=True)


class ColorFormatter(logging.Formatter):
    """Formata mensagens com cores ANSI para o console."""

    COLORS = {
        logging.DEBUG: "\033[94m",
        logging.INFO: "\033[92m",
        logging.WARNING: "\033[93m",
        logging.ERROR: "\033[91m",
        logging.CRITICAL: "\033[95m",
    }
    RESET = "\033[0m"

    def format(self, record: logging.LogRecord) -> str:
        color = self.COLORS.get(record.levelno, "")
        message = super().format(record)
        return f"{color}{message}{self.RESET}" if color else message


def get_logger(name: Optional[str] = None, level: str = "INFO") -> logging.Logger:
    """Cria ou recupera um logger configurado."""

    logger = logging.getLogger(name if name else __name__)
    if logger.handlers:
        return logger

    logger.setLevel(level)

    timestamp = datetime.now().strftime("%Y-%m-%d")
    file_path = os.path.join(LOG_DIR, f"coleta_{timestamp}.log")

    file_handler = logging.FileHandler(file_path, encoding="utf-8")
    file_handler.setFormatter(
        logging.Formatter("%(asctime)s [%(levelname)s] %(name)s - %(message)s")
    )

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(
        ColorFormatter("%(asctime)s [%(levelname)s] %(name)s - %(message)s")
    )

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    logger.propagate = False

    return logger
