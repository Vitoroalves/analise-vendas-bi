# analise-vendas-bi

Análise de vendas utilizando Python, SQL e Power BI.

Pipeline completo de BI sobre uma base sintética de vendas: geração dos dados,
limpeza/tratamento, análise exploratória em Python (pandas + matplotlib), as
mesmas análises reproduzidas em SQL sobre um banco SQLite, e um modelo estrela
pronto para consumo em um dashboard Power BI.

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
    powerbi/               Modelo estrela (fato + dimensões) pronto para o Power BI
notebooks/
  01_exploracao_inicial.py   Primeira exploração da base bruta
  02_analise_exploratoria.py Análise completa em pandas + gráficos + geração dos resumos
  03_analise_sql.py          As mesmas análises, via SQL (lê data/processed/vendas.db)
scripts/
  gerar_dados.py         Gera a base sintética de vendas (data/raw/vendas_raw.csv)
  limpar_dados.py        Limpa e trata os dados brutos (data/processed/vendas_tratadas.csv)
  criar_banco.py         Carrega os dados tratados no SQLite (data/processed/vendas.db)
  criar_modelo_estrela.py Gera o modelo estrela para Power BI (data/processed/powerbi/)
sql/
  consultas.sql           Consultas SQL comentadas (indicadores, rankings, séries mensais)
POWERBI.md                Guia passo a passo para montar o dashboard no Power BI Desktop
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

7. Gerar o modelo estrela para o Power BI:

   ```
   python scripts/criar_modelo_estrela.py
   ```

   Depois, seguir o passo a passo em [POWERBI.md](POWERBI.md) para montar o
   dashboard no Power BI Desktop.

## O que a análise cobre

- Faturamento, custo, lucro, margem, total de pedidos e clientes, ticket médio
- Produtos mais vendidos, por faturamento e por lucro
- Desempenho por categoria, região e estado
- Evolução mensal do faturamento
- Produtos com maior margem de lucro

## Dashboard Power BI

Dashboard completo com 4 páginas:

1. **Visão Geral** - KPIs principais (Faturamento: R$ 16,29 Mi, Lucro: R$ 4,28 Mi, Margem: 26%), evolução mensal, análise por categoria e região
2. **Produtos** - Análise detalhada dos 17 produtos, tabela completa, top 10, análise de margem por produto
3. **Geografia** - Análise das 5 regiões e 27 estados, tabelas e gráficos comparativos
4. **Melhorias** - Insights estratégicos, produtos com baixa margem, tendências e recomendações

### Principais Insights:

- ✅ Eletrônicos representa 55% do faturamento total
- ✅ Sudeste lidera com 40% do faturamento
- ✅ Smartphone é o produto mais lucrativo
- ⚠️ 3 produtos com margem abaixo de 25% precisam de revisão
- 💡 Norte apresenta a melhor margem de lucro por região

O arquivo `.pbix` está salvo na raiz do projeto.
