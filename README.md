# analise-vendas-bi

Análise de vendas utilizando Python, SQL e Power BI.

Pipeline completo de BI sobre uma base sintética de vendas: geração dos dados,
limpeza/tratamento, análise exploratória em Python (pandas + matplotlib) e as
mesmas análises reproduzidas em SQL sobre um banco SQLite.

## Estrutura do projeto

```
data/
  raw/                  Dados brutos (gerados por scripts/gerar_dados.py)
  processed/             Dados tratados e resumos de análise
    vendas_tratadas.csv  Base limpa, com colunas calculadas (faturamento, lucro, margem...)
    vendas.db             Banco SQLite usado pela camada de análise SQL
    resumo_produtos.csv
    resumo_categorias.csv
    resumo_regioes.csv
    vendas_mensais.csv
notebooks/
  01_exploracao_inicial.py   Primeira exploração da base bruta
  02_analise_exploratoria.py Análise completa em pandas + gráficos + geração dos resumos
  03_analise_sql.py          As mesmas análises, via SQL (lê data/processed/vendas.db)
scripts/
  gerar_dados.py         Gera a base sintética de vendas (data/raw/vendas_raw.csv)
  limpar_dados.py        Limpa e trata os dados brutos (data/processed/vendas_tratadas.csv)
  criar_banco.py         Carrega os dados tratados no SQLite (data/processed/vendas.db)
sql/
  consultas.sql           Consultas SQL comentadas (indicadores, rankings, séries mensais)
```

## Como rodar

1. Criar e ativar um ambiente virtual, depois instalar as dependências:

   ```
   python -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. Gerar a base de dados bruta:

   ```
   python scripts/gerar_dados.py
   ```

3. Limpar e tratar os dados:

   ```
   python scripts/limpar_dados.py
   ```

4. Rodar a análise exploratória em Python (gera os gráficos e os CSVs de resumo):

   ```
   python notebooks/02_analise_exploratoria.py
   ```

5. Criar o banco SQLite a partir dos dados tratados:

   ```
   python scripts/criar_banco.py
   ```

6. Rodar a análise em SQL:

   ```
   python notebooks/03_analise_sql.py
   ```

   Ou explorar as consultas diretamente com o CLI do SQLite:

   ```
   sqlite3 data/processed/vendas.db
   .read sql/consultas.sql
   ```

## O que a análise cobre

- Faturamento, custo, lucro, margem, total de pedidos e clientes, ticket médio
- Produtos mais vendidos, por faturamento e por lucro
- Desempenho por categoria, região e estado
- Evolução mensal do faturamento
- Produtos com maior margem de lucro

## Próximos passos

- Dashboard em Power BI consumindo os dados de `data/processed/`
