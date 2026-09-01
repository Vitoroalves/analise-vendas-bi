import pandas as pd
import matplotlib.pyplot as plt


# ============================================================
# CARREGAR DADOS
# ============================================================

arquivo = "data/processed/vendas_tratadas.csv"

df = pd.read_csv(arquivo)

print("=" * 60)
print("ESTRUTURA DOS DADOS")
print("=" * 60)

print(f"Linhas: {df.shape[0]}")
print(f"Colunas: {df.shape[1]}")

print("\nColunas:")
print(df.columns.tolist())


faturamento_total = df["faturamento"].sum()
print("\nFaturamento total:")
print(f"R$ {faturamento_total:,.2f}")


custo_total = df["custo_total"].sum()
print("\nCusto total:")
print(f"R$ {custo_total:,.2f}")


lucro_total = df["lucro"].sum()
print("\nLucro total:")
print(f"R$ {lucro_total:,.2f}")


margem_total = (
    lucro_total / faturamento_total
)
print("\nMargem de lucro:")
print(f"{margem_total:.2%}")


total_pedidos = df["id_pedido"].nunique()
print("\nTotal de pedidos:")
print(total_pedidos)


total_clientes = df["id_cliente"].nunique()
print("\nTotal de clientes:")
print(total_clientes)


ticket_medio = (
    faturamento_total / total_pedidos
)
print("\nTicket médio:")
print(f"R$ {ticket_medio:,.2f}")


print("\n" + "=" * 60)
print("INDICADORES GERAIS")
print("=" * 60)

print(f"Pedidos: {total_pedidos:,}")
print(f"Clientes: {total_clientes:,}")
print(f"Faturamento: R$ {faturamento_total:,.2f}")
print(f"Custo: R$ {custo_total:,.2f}")
print(f"Lucro: R$ {lucro_total:,.2f}")
print(f"Margem: {margem_total:.2%}")
print(f"Ticket médio: R$ {ticket_medio:,.2f}")


produtos_mais_vendidos = (
    df["produto"]
    .value_counts()
    .head(10)
)
print("\n" + "=" * 60)
print("TOP 10 PRODUTOS MAIS VENDIDOS")
print("=" * 60)
print(produtos_mais_vendidos)


faturamento_produtos = (
    df.groupby("produto")["faturamento"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)
print("\n" + "=" * 60)
print("TOP 10 PRODUTOS POR FATURAMENTO")
print("=" * 60)

print(faturamento_produtos)


lucro_produtos = (
    df.groupby("produto")["lucro"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print("\n" + "=" * 60)
print("TOP 10 PRODUTOS POR LUCRO")
print("=" * 60)

print(lucro_produtos)


categoria_vendas = (
    df.groupby("categoria")
    .agg(
        pedidos=("id_pedido", "nunique"),
        faturamento=("faturamento", "sum"),
        lucro=("lucro", "sum"),
        quantidade=("quantidade", "sum"),
    )
    .sort_values(
        "faturamento",
        ascending=False
    )
)

print("\n" + "=" * 60)
print("ANÁLISE POR CATEGORIA")
print("=" * 60)

print(categoria_vendas)

categoria_vendas["margem"] = (
    categoria_vendas["lucro"]
    / categoria_vendas["faturamento"]
)

print("\nMargem por categoria:")
print(
    categoria_vendas[
        ["faturamento", "lucro", "margem"]
    ]
)


regiao_vendas = (
    df.groupby("regiao")
    .agg(
        pedidos=("id_pedido", "nunique"),
        faturamento=("faturamento", "sum"),
        lucro=("lucro", "sum"),
        quantidade=("quantidade", "sum"),
    )
    .sort_values(
        "faturamento",
        ascending=False
    )
)

print("\n" + "=" * 60)
print("ANÁLISE POR REGIÃO")
print("=" * 60)

print(regiao_vendas)

regiao_vendas["margem"] = (
    regiao_vendas["lucro"]
    / regiao_vendas["faturamento"]
)

print("\nMargem por região:")
print(
    regiao_vendas[
        ["faturamento", "lucro", "margem"]
    ]
)

estado_vendas = (
    df.groupby("estado")
    .agg(
        pedidos=("id_pedido", "nunique"),
        faturamento=("faturamento", "sum"),
        lucro=("lucro", "sum"),
    )
    .sort_values(
        "faturamento",
        ascending=False
    )
)

print("\n" + "=" * 60)
print("TOP ESTADOS POR FATURAMENTO")
print("=" * 60)

print(estado_vendas.head(10))


vendas_mensais = (
    df.groupby(
        ["ano", "mes"]
    )
    .agg(
        pedidos=("id_pedido", "nunique"),
        faturamento=("faturamento", "sum"),
        lucro=("lucro", "sum"),
    )
    .reset_index()
)

print("\n" + "=" * 60)
print("VENDAS POR MÊS")
print("=" * 60)

print(vendas_mensais)


faturamento_anual = (
    df.groupby("ano")["faturamento"]
    .sum()
)

print("\n" + "=" * 60)
print("FATURAMENTO POR ANO")
print("=" * 60)

print(faturamento_anual)


faturamento_mensal = (
    df.groupby("mes")["faturamento"]
    .sum()
)

print("\n" + "=" * 60)
print("FATURAMENTO POR MÊS")
print("=" * 60)

print(faturamento_mensal)


# ============================================================
# GRÁFICO — EVOLUÇÃO DO FATURAMENTO POR MÊS (Etapa 26)
# ============================================================

faturamento_mensal = (
    df.groupby("mes")["faturamento"]
    .sum()
    .sort_index()
)

plt.figure(figsize=(10, 5))

plt.plot(
    faturamento_mensal.index,
    faturamento_mensal.values,
    marker="o"
)

plt.title("Evolução do faturamento por mês")
plt.xlabel("Mês")
plt.ylabel("Faturamento")

plt.xticks(range(1, 13))

plt.grid(True, alpha=0.3)

plt.tight_layout()

plt.show()


# ============================================================
# GRÁFICO — FATURAMENTO POR CATEGORIA (Etapa 27)
# ============================================================

plt.figure(figsize=(10, 5))

plt.bar(
    categoria_vendas.index,
    categoria_vendas["faturamento"]
)

plt.title("Faturamento por categoria")
plt.xlabel("Categoria")
plt.ylabel("Faturamento")

plt.xticks(rotation=20)

plt.tight_layout()

plt.show()


# ============================================================
# GRÁFICO — TOP 10 PRODUTOS POR FATURAMENTO (Etapa 28)
# ============================================================

top_produtos = (
    faturamento_produtos
    .sort_values()
)

plt.figure(figsize=(10, 6))

plt.barh(
    top_produtos.index,
    top_produtos.values
)

plt.title("Top 10 produtos por faturamento")
plt.xlabel("Faturamento")
plt.ylabel("Produto")

plt.tight_layout()

plt.show()


# ============================================================
# MARGEM POR PRODUTO (Etapa 30)
# ============================================================

margem_produtos = (
    df.groupby("produto")
    .agg(
        faturamento=("faturamento", "sum"),
        lucro=("lucro", "sum")
    )
)

margem_produtos["margem"] = (
    margem_produtos["lucro"]
    / margem_produtos["faturamento"]
)

margem_produtos = (
    margem_produtos
    .sort_values("margem", ascending=False)
)

print("\n" + "=" * 60)
print("PRODUTOS COM MAIOR MARGEM")
print("=" * 60)

print(margem_produtos)


# ============================================================
# RESUMO DOS PRODUTOS (Etapa 32)
# ============================================================

resumo_produtos = (
    df.groupby("produto")
    .agg(
        pedidos=("id_pedido", "nunique"),
        unidades=("quantidade", "sum"),
        faturamento=("faturamento", "sum"),
        lucro=("lucro", "sum"),
    )
)

resumo_produtos["margem"] = (
    resumo_produtos["lucro"]
    / resumo_produtos["faturamento"]
)

resumo_produtos = (
    resumo_produtos
    .sort_values("faturamento", ascending=False)
)

print("\n" + "=" * 60)
print("RESUMO DOS PRODUTOS")
print("=" * 60)

print(resumo_produtos)


# ============================================================
# MELHOR PRODUTO (Etapa 33)
# ============================================================

melhor_produto_faturamento = (
    resumo_produtos["faturamento"]
    .idxmax()
)

print("\nProduto com maior faturamento:")
print(melhor_produto_faturamento)

melhor_produto_lucro = (
    resumo_produtos["lucro"]
    .idxmax()
)

print("\nProduto com maior lucro:")
print(melhor_produto_lucro)


# ============================================================
# MELHOR CATEGORIA (Etapa 34)
# ============================================================

melhor_categoria = (
    categoria_vendas["faturamento"]
    .idxmax()
)

print("\nCategoria com maior faturamento:")
print(melhor_categoria)

melhor_categoria_lucro = (
    categoria_vendas["lucro"]
    .idxmax()
)

print("\nCategoria com maior lucro:")
print(melhor_categoria_lucro)


# ============================================================
# MELHOR REGIÃO (Etapa 35)
# ============================================================

melhor_regiao = (
    regiao_vendas["faturamento"]
    .idxmax()
)

print("\nRegião com maior faturamento:")
print(melhor_regiao)


# ============================================================
# RESUMO EXECUTIVO (Etapa 36)
# ============================================================

print("\n" + "=" * 60)
print("RESUMO EXECUTIVO")
print("=" * 60)

print(f"Faturamento total: R$ {faturamento_total:,.2f}")
print(f"Lucro total: R$ {lucro_total:,.2f}")
print(f"Margem de lucro: {margem_total:.2%}")
print(f"Pedidos: {total_pedidos:,}")
print(f"Clientes: {total_clientes:,}")
print(f"Ticket médio: R$ {ticket_medio:,.2f}")
print(f"Produto líder em faturamento: {melhor_produto_faturamento}")
print(f"Categoria líder em faturamento: {melhor_categoria}")
print(f"Região líder em faturamento: {melhor_regiao}")


# ============================================================
# SALVAR RESULTADOS (Etapa 38)
# ============================================================

resumo_produtos.to_csv(
    "data/processed/resumo_produtos.csv"
)

categoria_vendas.to_csv(
    "data/processed/resumo_categorias.csv"
)

regiao_vendas.to_csv(
    "data/processed/resumo_regioes.csv"
)

vendas_mensais.to_csv(
    "data/processed/vendas_mensais.csv",
    index=False
)

print("\nArquivos salvos em data/processed/")
