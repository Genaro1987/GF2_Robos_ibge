"""Validadores e saneamento de dados de entrada."""
from __future__ import annotations

import re
from typing import Any, Optional

IBGE_REGEX = re.compile(r"^\d{7}$")


def validar_codigo_ibge(codigo: str) -> bool:
    """Valida se o código IBGE possui 7 dígitos."""

    return bool(IBGE_REGEX.match(codigo))


def validar_ano(ano: int, minimo: int = 1900, maximo: int = 2100) -> bool:
    """Valida se o ano está no intervalo permitido."""

    return minimo <= int(ano) <= maximo


def limpar_valor(valor: Optional[str]) -> Optional[float]:
    """Converte strings numéricas para float, retornando None para vazios."""

    if valor in (None, "", "-"):
        return None
    try:
        return float(str(valor).replace(",", "."))
    except ValueError:
        return None


def valor_nao_negativo(valor: Optional[float]) -> Optional[float]:
    """Garante que valores negativos sejam tratados como None."""

    if valor is None:
        return None
    return valor if valor >= 0 else None


def preparar_numero(valor: Any) -> Optional[float]:
    """Processa um valor numérico simples garantindo ausência de negativos."""

    return valor_nao_negativo(limpar_valor(valor))
