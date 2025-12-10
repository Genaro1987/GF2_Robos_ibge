# Robôs IBGE para MySQL

Sistema completo em Python para coletar dados do IBGE (SIDRA, Agregados e Atlas Brasil) e popular tabelas analíticas em um banco MySQL já existente com cadastros de municípios e empresas.

## Pré-requisitos
- Python 3.10+
- MySQL 8+
- Acesso à tabela existente `dim_ibge_municipios` com os municípios brasileiros (7 dígitos)
- Sistema operacional com acesso à internet para as APIs públicas do IBGE

## Instalação
1. Clone o repositório e acesse a pasta `robos_ibge/`.
2. Crie um ambiente virtual e instale as dependências:
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r robos_ibge/requirements.txt
   ```
3. Copie o arquivo `.env.example` para `.env` e ajuste as credenciais do banco e parâmetros de coleta.

## Configuração
- `DB_HOST`, `DB_USER`, `DB_PASSWORD`, `DB_NAME`, `DB_CHARSET`: credenciais do MySQL.
- `LOG_LEVEL`: nível de log (INFO/DEBUG).
- `IBGE_TIMEOUT`: timeout das requisições HTTP.
- `BATCH_SIZE`: tamanho dos lotes de INSERT.

## Setup inicial
Execute o script de setup para validar o ambiente, criar tabelas e conferir a base de municípios:
```bash
python -m robos_ibge.setup
```

## Uso da CLI
No diretório `robos_ibge/`, execute:
```bash
python -m robos_ibge.main --todos
python -m robos_ibge.main --demografico --anos 2022,2023,2024
python -m robos_ibge.main --pib --teste
python -m robos_ibge.main --socioeconomico --atlas-csv data/atlas.csv
python -m robos_ibge.main --infraestrutura --verbose
```
- `--todos`: executa todos os coletores.
- `--teste`: limita a 10 municípios para validação rápida.
- `--anos`: filtra os anos desejados.
- `--verbose`: aumenta verbosidade de log.

## Estrutura do projeto
```
robos_ibge/
├── api_clients/
├── coletores/
├── config/
├── database/
├── utils/
├── logs/ (gitignored)
└── data/ (gitignored)
```

## APIs utilizadas
- **SIDRA**: https://apisidra.ibge.gov.br/values (tabelas 6579, 5938, 1384, 5370)
- **Agregados IBGE**: https://servicodados.ibge.gov.br/api/v3/agregados
- **Atlas Brasil**: consumo via CSV exportado (anos 2010, 2021)

## Funcionalidades principais
- Logging diário com cores no console.
- Retentativas automáticas com backoff exponencial.
- Inserções em lote com UPSERT (`ON DUPLICATE KEY UPDATE`).
- Validações de códigos IBGE e anos.
- Barra de progresso com `tqdm`.

## Troubleshooting
- **Falha de conexão MySQL**: confira host, porta e plugin `mysql_native_password` habilitado.
- **Tabela de municípios vazia**: preencha `dim_ibge_municipios` antes de rodar os robôs.
- **Atlas Brasil**: se não houver API disponível, exporte um CSV e informe via `--atlas-csv`.
- **Limite de requisições**: use `--teste` para amostragens pequenas durante ajustes.

## Roadmap
- Acrescentar cálculo de densidade demográfica com área territorial.
- Melhorar cobertura de variáveis de saúde e educação com novas tabelas SIDRA.
- Adicionar orquestração com `schedule` para execuções periódicas.
- Implementar suporte direto à API oficial do Atlas Brasil, quando disponível.
