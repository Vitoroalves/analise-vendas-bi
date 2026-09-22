import sqlite3
from pathlib import Path

import pandas as pd


# ============================================================
# CONEXÃO COM O BANCO
# ============================================================

arquivo_banco = Path("data/processed/vendas.db")

if not arquivo_banco.exists():
    raise FileNotFoundError(
        "Banco não encontrado. Rode antes: "
        "python scripts/criar_banco.py"
    )

conexao = sqlite3.connect(arquivo_banco)


# ============================================================
# INDICADORES GERAIS
# ============================================================

indicadores = pd.read_sql_query(
    """
    SELECT
        ROUND(SUM(faturamento), 2) AS faturamento_total,
        ROUND(SUM(custo_total), 2) AS custo_total,
        ROUND(SUM(lucro), 2) AS lucro_total,
        ROUND(SUM(lucro) * 1.0 / SUM(faturamento), 4) AS margem_lucro,
        COUNT(DISTINCT id_pedido) AS total_pedidos,
        COUNT(DISTINCT id_cliente) AS total_clientes,
        ROUND(SUM(faturamento) * 1.0 / COUNT(DISTINCT id_pedido), 2) AS ticket_medio
    FROM vendas
    """,
    conexao,
).iloc[0]

print("=" * 60)
print("INDICADORES GERAIS (via SQL)")
print("=" * 60)

print(f"Faturamento total: R$ {indicadores['faturamento_total']:,.2f}")
print(f"Custo total: R$ {indicadores['custo_total']:,.2f}")
print(f"Lucro total: R$ {indicadores['lucro_total']:,.2f}")
print(f"Margem de lucro: {indicadores['margem_lucro']:.2%}")
print(f"Pedidos: {int(indicadores['total_pedidos']):,}")
print(f"Clientes: {int(indicadores['total_clientes']):,}")
print(f"Ticket médio: R$ {indicadores['ticket_medio']:,.2f}")


# ============================================================
# TOP 10 PRODUTOS POR FATURAMENTO
# ============================================================

top_produtos_faturamento = pd.read_sql_query(
    """
    SELECT
        produto,
        ROUND(SUM(faturamento), 2) AS faturamento
    FROM vendas
    GROUP BY produto
    ORDER BY faturamento DESC
    LIMIT 10
    """,
    conexao,
)

print("\n" + "=" * 60)
print("TOP 10 PRODUTOS POR FATURAMENTO")
print("=" * 60)
print(top_produtos_faturamento.to_string(index=False))


# ============================================================
# TOP 10 PRODUTOS POR LUCRO
# ============================================================

top_produtos_lucro = pd.read_sql_query(
    """
    SELECT
        produto,
        ROUND(SUM(lucro), 2) AS lucro
    FROM vendas
    GROUP BY produto
    ORDER BY lucro DESC
    LIMIT 10
    """,
    conexao,
)

print("\n" + "=" * 60)
print("TOP 10 PRODUTOS POR LUCRO")
print("=" * 60)
print(top_produtos_lucro.to_string(index=False))


# ============================================================
# ANÁLISE POR CATEGORIA
# ============================================================

categoria_vendas = pd.read_sql_query(
    """
    SELECT
        categoria,
        COUNT(DISTINCT id_pedido) AS pedidos,
        ROUND(SUM(faturamento), 2) AS faturamento,
        ROUND(SUM(lucro), 2) AS lucro,
        SUM(quantidade) AS quantidade,
        ROUND(SUM(lucro) * 1.0 / SUM(faturamento), 4) AS margem
    FROM vendas
    GROUP BY categoria
    ORDER BY faturamento DESC
    """,
    conexao,
)

print("\n" + "=" * 60)
print("ANÁLISE POR CATEGORIA")
print("=" * 60)
print(categoria_vendas.to_string(index=False))


# ============================================================
# ANÁLISE POR REGIÃO
# ============================================================

regiao_vendas = pd.read_sql_query(
    """
    SELECT
        regiao,
        COUNT(DISTINCT id_pedido) AS pedidos,
        ROUND(SUM(faturamento), 2) AS faturamento,
        ROUND(SUM(lucro), 2) AS lucro,
        SUM(quantidade) AS quantidade,
        ROUND(SUM(lucro) * 1.0 / SUM(faturamento), 4) AS margem
    FROM vendas
    GROUP BY regiao
    ORDER BY faturamento DESC
    """,
    conexao,
)

print("\n" + "=" * 60)
print("ANÁLISE POR REGIÃO")
print("=" * 60)
print(regiao_vendas.to_string(index=False))


# ============================================================
# TOP 10 ESTADOS POR FATURAMENTO
# ============================================================

estado_vendas = pd.read_sql_query(
    """
    SELECT
        estado,
        COUNT(DISTINCT id_pedido) AS pedidos,
        ROUND(SUM(faturamento), 2) AS faturamento,
        ROUND(SUM(lucro), 2) AS lucro
    FROM vendas
    GROUP BY estado
    ORDER BY faturamento DESC
    LIMIT 10
    """,
    conexao,
)

print("\n" + "=" * 60)
print("TOP 10 ESTADOS POR FATURAMENTO")
print("=" * 60)
print(estado_vendas.to_string(index=False))


# ============================================================
# VENDAS POR MÊS
# ============================================================

vendas_mensais = pd.read_sql_query(
    """
    SELECT
        ano,
        mes,
        COUNT(DISTINCT id_pedido) AS pedidos,
        ROUND(SUM(faturamento), 2) AS faturamento,
        ROUND(SUM(lucro), 2) AS lucro
    FROM vendas
    GROUP BY ano, mes
    ORDER BY ano, mes
    """,
    conexao,
)

print("\n" + "=" * 60)
print("VENDAS POR MÊS")
print("=" * 60)
print(vendas_mensais.to_string(index=False))


# ============================================================
# PRODUTOS COM MAIOR MARGEM
# ============================================================

margem_produtos = pd.read_sql_query(
    """
    SELECT
        produto,
        ROUND(SUM(faturamento), 2) AS faturamento,
        ROUND(SUM(lucro), 2) AS lucro,
        ROUND(SUM(lucro) * 1.0 / SUM(faturamento), 4) AS margem
    FROM vendas
    GROUP BY produto
    ORDER BY margem DESC
    """,
    conexao,
)

print("\n" + "=" * 60)
print("PRODUTOS COM MAIOR MARGEM")
print("=" * 60)
print(margem_produtos.to_string(index=False))


# ============================================================
# DESTAQUES (produto, categoria e região líderes)
# ============================================================

melhor_produto_faturamento = top_produtos_faturamento.iloc[0]["produto"]
melhor_produto_lucro = top_produtos_lucro.iloc[0]["produto"]
melhor_categoria = categoria_vendas.iloc[0]["categoria"]
melhor_categoria_lucro = categoria_vendas.sort_values(
    "lucro", ascending=False
).iloc[0]["categoria"]
melhor_regiao = regiao_vendas.iloc[0]["regiao"]

print("\n" + "=" * 60)
print("RESUMO EXECUTIVO (via SQL)")
print("=" * 60)

print(f"Faturamento total: R$ {indicadores['faturamento_total']:,.2f}")
print(f"Lucro total: R$ {indicadores['lucro_total']:,.2f}")
print(f"Margem de lucro: {indicadores['margem_lucro']:.2%}")
print(f"Pedidos: {int(indicadores['total_pedidos']):,}")
print(f"Clientes: {int(indicadores['total_clientes']):,}")
print(f"Ticket médio: R$ {indicadores['ticket_medio']:,.2f}")
print(f"Produto líder em faturamento: {melhor_produto_faturamento}")
print(f"Produto líder em lucro: {melhor_produto_lucro}")
print(f"Categoria líder em faturamento: {melhor_categoria}")
print(f"Categoria líder em lucro: {melhor_categoria_lucro}")
print(f"Região líder em faturamento: {melhor_regiao}")

conexao.close()
