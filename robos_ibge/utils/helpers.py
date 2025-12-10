"""Funções auxiliares diversas."""
from __future__ import annotations

from typing import Iterable, List


def dividir_em_lotes(iteravel: Iterable, tamanho: int) -> List[list]:
    """Divide um iterável em lotes de tamanho informado."""

    lote: list = []
    lotes: List[list] = []
    for item in iteravel:
        lote.append(item)
        if len(lote) >= tamanho:
            lotes.append(lote)
            lote = []
    if lote:
        lotes.append(lote)
    return lotes
