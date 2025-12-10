"""Consultas SQL reutilizáveis para operações de coleta."""
from __future__ import annotations

from typing import Dict


CREATE_TABLES: Dict[str, str] = {}


INSERT_DEMOGRAFICO = (
    """
    INSERT INTO dim_ibge_demografico (
        dem_ibge_codigo, dem_ano, dem_pop_total, dem_pop_urbana, dem_pop_rural,
        dem_pop_homens, dem_pop_mulheres, dem_densidade_demografica,
        dem_pop_0_14, dem_pop_15_64, dem_pop_65_mais, dem_taxa_crescimento,
        dem_fonte, dem_criado_em, dem_atualizado_em
    ) VALUES (
        %(dem_ibge_codigo)s, %(dem_ano)s, %(dem_pop_total)s, %(dem_pop_urbana)s, %(dem_pop_rural)s,
        %(dem_pop_homens)s, %(dem_pop_mulheres)s, %(dem_densidade_demografica)s,
        %(dem_pop_0_14)s, %(dem_pop_15_64)s, %(dem_pop_65_mais)s, %(dem_taxa_crescimento)s,
        %(dem_fonte)s, NOW(), NOW()
    ) ON DUPLICATE KEY UPDATE
        dem_pop_total = VALUES(dem_pop_total),
        dem_pop_urbana = VALUES(dem_pop_urbana),
        dem_pop_rural = VALUES(dem_pop_rural),
        dem_pop_homens = VALUES(dem_pop_homens),
        dem_pop_mulheres = VALUES(dem_pop_mulheres),
        dem_densidade_demografica = VALUES(dem_densidade_demografica),
        dem_pop_0_14 = VALUES(dem_pop_0_14),
        dem_pop_15_64 = VALUES(dem_pop_15_64),
        dem_pop_65_mais = VALUES(dem_pop_65_mais),
        dem_taxa_crescimento = VALUES(dem_taxa_crescimento),
        dem_fonte = VALUES(dem_fonte),
        dem_atualizado_em = NOW();
    """
)

INSERT_PIB = (
    """
    INSERT INTO dim_ibge_pib_municipal (
        pib_ibge_codigo, pib_ano, pib_total, pib_per_capita, pib_agropecuaria,
        pib_industria, pib_servicos, pib_administracao_publica, pib_impostos,
        pib_va_total, pib_fonte, pib_criado_em, pib_atualizado_em
    ) VALUES (
        %(pib_ibge_codigo)s, %(pib_ano)s, %(pib_total)s, %(pib_per_capita)s, %(pib_agropecuaria)s,
        %(pib_industria)s, %(pib_servicos)s, %(pib_administracao_publica)s, %(pib_impostos)s,
        %(pib_va_total)s, %(pib_fonte)s, NOW(), NOW()
    ) ON DUPLICATE KEY UPDATE
        pib_total = VALUES(pib_total),
        pib_per_capita = VALUES(pib_per_capita),
        pib_agropecuaria = VALUES(pib_agropecuaria),
        pib_industria = VALUES(pib_industria),
        pib_servicos = VALUES(pib_servicos),
        pib_administracao_publica = VALUES(pib_administracao_publica),
        pib_impostos = VALUES(pib_impostos),
        pib_va_total = VALUES(pib_va_total),
        pib_fonte = VALUES(pib_fonte),
        pib_atualizado_em = NOW();
    """
)

INSERT_SOCIO = (
    """
    INSERT INTO dim_ibge_indices_socioeconomicos (
        idx_ibge_codigo, idx_ano, idx_idhm, idx_idhm_renda, idx_idhm_longevidade,
        idx_idhm_educacao, idx_renda_per_capita, idx_gini, idx_percentual_pobres,
        idx_percentual_extrema_pobreza, idx_taxa_alfabetizacao, idx_anos_estudo_medio,
        idx_frequencia_escolar_6_14, idx_taxa_desemprego, idx_taxa_formalizacao,
        idx_esperanca_vida, idx_mortalidade_infantil, idx_fonte, idx_criado_em, idx_atualizado_em
    ) VALUES (
        %(idx_ibge_codigo)s, %(idx_ano)s, %(idx_idhm)s, %(idx_idhm_renda)s, %(idx_idhm_longevidade)s,
        %(idx_idhm_educacao)s, %(idx_renda_per_capita)s, %(idx_gini)s, %(idx_percentual_pobres)s,
        %(idx_percentual_extrema_pobreza)s, %(idx_taxa_alfabetizacao)s, %(idx_anos_estudo_medio)s,
        %(idx_frequencia_escolar_6_14)s, %(idx_taxa_desemprego)s, %(idx_taxa_formalizacao)s,
        %(idx_esperanca_vida)s, %(idx_mortalidade_infantil)s, %(idx_fonte)s, NOW(), NOW()
    ) ON DUPLICATE KEY UPDATE
        idx_idhm = VALUES(idx_idhm),
        idx_idhm_renda = VALUES(idx_idhm_renda),
        idx_idhm_longevidade = VALUES(idx_idhm_longevidade),
        idx_idhm_educacao = VALUES(idx_idhm_educacao),
        idx_renda_per_capita = VALUES(idx_renda_per_capita),
        idx_gini = VALUES(idx_gini),
        idx_percentual_pobres = VALUES(idx_percentual_pobres),
        idx_percentual_extrema_pobreza = VALUES(idx_percentual_extrema_pobreza),
        idx_taxa_alfabetizacao = VALUES(idx_taxa_alfabetizacao),
        idx_anos_estudo_medio = VALUES(idx_anos_estudo_medio),
        idx_frequencia_escolar_6_14 = VALUES(idx_frequencia_escolar_6_14),
        idx_taxa_desemprego = VALUES(idx_taxa_desemprego),
        idx_taxa_formalizacao = VALUES(idx_taxa_formalizacao),
        idx_esperanca_vida = VALUES(idx_esperanca_vida),
        idx_mortalidade_infantil = VALUES(idx_mortalidade_infantil),
        idx_fonte = VALUES(idx_fonte),
        idx_atualizado_em = NOW();
    """
)

INSERT_INFRA = (
    """
    INSERT INTO dim_ibge_infraestrutura (
        inf_ibge_codigo, inf_ano, inf_abastecimento_agua, inf_esgotamento_sanitario,
        inf_coleta_lixo, inf_energia_eletrica, inf_leitos_hospitalares,
        inf_leitos_por_1000_hab, inf_estabelecimentos_saude, inf_medicos_por_1000_hab,
        inf_escolas_fundamental, inf_escolas_medio, inf_escolas_superior,
        inf_agencias_bancarias, inf_correios, inf_fonte, inf_criado_em, inf_atualizado_em
    ) VALUES (
        %(inf_ibge_codigo)s, %(inf_ano)s, %(inf_abastecimento_agua)s, %(inf_esgotamento_sanitario)s,
        %(inf_coleta_lixo)s, %(inf_energia_eletrica)s, %(inf_leitos_hospitalares)s,
        %(inf_leitos_por_1000_hab)s, %(inf_estabelecimentos_saude)s, %(inf_medicos_por_1000_hab)s,
        %(inf_escolas_fundamental)s, %(inf_escolas_medio)s, %(inf_escolas_superior)s,
        %(inf_agencias_bancarias)s, %(inf_correios)s, %(inf_fonte)s, NOW(), NOW()
    ) ON DUPLICATE KEY UPDATE
        inf_abastecimento_agua = VALUES(inf_abastecimento_agua),
        inf_esgotamento_sanitario = VALUES(inf_esgotamento_sanitario),
        inf_coleta_lixo = VALUES(inf_coleta_lixo),
        inf_energia_eletrica = VALUES(inf_energia_eletrica),
        inf_leitos_hospitalares = VALUES(inf_leitos_hospitalares),
        inf_leitos_por_1000_hab = VALUES(inf_leitos_por_1000_hab),
        inf_estabelecimentos_saude = VALUES(inf_estabelecimentos_saude),
        inf_medicos_por_1000_hab = VALUES(inf_medicos_por_1000_hab),
        inf_escolas_fundamental = VALUES(inf_escolas_fundamental),
        inf_escolas_medio = VALUES(inf_escolas_medio),
        inf_escolas_superior = VALUES(inf_escolas_superior),
        inf_agencias_bancarias = VALUES(inf_agencias_bancarias),
        inf_correios = VALUES(inf_correios),
        inf_fonte = VALUES(inf_fonte),
        inf_atualizado_em = NOW();
    """
)


def get_insert_query(tipo: str) -> str:
    """Obtém a query de inserção baseada no tipo solicitado."""

    mapping = {
        "demografico": INSERT_DEMOGRAFICO,
        "pib": INSERT_PIB,
        "socioeconomico": INSERT_SOCIO,
        "infraestrutura": INSERT_INFRA,
    }
    if tipo not in mapping:
        raise KeyError(f"Tipo de coleta desconhecido: {tipo}")
    return mapping[tipo]
