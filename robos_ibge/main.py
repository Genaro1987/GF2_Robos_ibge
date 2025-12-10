"""Ponto de entrada principal para executar os robôs de coleta IBGE."""
from __future__ import annotations

import argparse
from typing import List

from robos_ibge.coletores.demografico_coletor import DemograficoColetor
from robos_ibge.coletores.infraestrutura_coletor import InfraestruturaColetor
from robos_ibge.coletores.pib_coletor import PibColetor
from robos_ibge.coletores.socioeconomico_coletor import SocioeconomicoColetor
from robos_ibge.config.settings import settings
from robos_ibge.database.connection import connection_manager
from robos_ibge.utils.logger import get_logger

LOGGER = get_logger(__name__, level=settings.log_level)


def parse_args() -> argparse.Namespace:
    """Configura o parser CLI."""

    parser = argparse.ArgumentParser(description="Coletas automáticas do IBGE")
    parser.add_argument("--todos", action="store_true", help="Executa todos os coletores")
    parser.add_argument("--demografico", action="store_true", help="Executa coleta demográfica")
    parser.add_argument("--pib", action="store_true", help="Executa coleta de PIB")
    parser.add_argument("--socioeconomico", action="store_true", help="Executa coleta socioeconômica")
    parser.add_argument("--infraestrutura", action="store_true", help="Executa coleta de infraestrutura")
    parser.add_argument("--anos", type=str, help="Lista de anos separados por vírgula")
    parser.add_argument("--teste", action="store_true", help="Executa apenas 10 municípios")
    parser.add_argument("--verbose", action="store_true", help="Força logs detalhados")
    parser.add_argument("--atlas-csv", dest="atlas_csv", type=str, help="Caminho para CSV do Atlas Brasil")
    return parser.parse_args()


def _anos_param(args: argparse.Namespace) -> List[int] | None:
    if not args.anos:
        return None
    return [int(item) for item in args.anos.split(",") if item.strip()]


def main() -> None:
    """Inicializa o ambiente e delega aos coletores selecionados."""

    args = parse_args()
    if args.verbose:
        LOGGER.setLevel("DEBUG")

    anos = _anos_param(args)
    connection_manager.init_pool()

    coletores = []
    if args.todos or args.demografico:
        coletores.append(DemograficoColetor(teste=args.teste, anos=anos))
    if args.todos or args.pib:
        coletores.append(PibColetor(teste=args.teste, anos=anos))
    if args.todos or args.socioeconomico:
        coletores.append(
            SocioeconomicoColetor(teste=args.teste, anos=anos, csv_path=args.atlas_csv)
        )
    if args.todos or args.infraestrutura:
        coletores.append(InfraestruturaColetor(teste=args.teste, anos=anos))

    if not coletores:
        LOGGER.warning("Nenhum coletor selecionado. Use --todos ou opções específicas.")
        return

    for coletor in coletores:
        LOGGER.info("Iniciando coletor: %s", coletor.tipo)
        coletor.processar()
        if coletor.erros:
            LOGGER.warning("Coletor %s finalizado com %d erros", coletor.tipo, len(coletor.erros))


if __name__ == "__main__":
    main()
