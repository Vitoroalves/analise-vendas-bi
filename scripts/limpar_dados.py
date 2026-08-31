import pandas as pd
from pathlib import Path


# ============================================================
# CONFIGURAÇÕES
# ============================================================

arquivo_entrada = Path("data/raw/vendas_raw.csv")
arquivo_saida = Path("data/processed/vendas_tratadas.csv")


# ============================================================
# LEITURA DOS DADOS
# ============================================================

df = pd.read_csv(arquivo_entrada)

print("=" * 60)
print("INFORMAÇÕES INICIAIS")
print("=" * 60)

print(f"Linhas: {df.shape[0]}")
print(f"Colunas: {df.shape[1]}")

print("\nColunas:")
print(df.columns.tolist())

print("\n" + "=" * 60)
print("VALORES NULOS")
print("=" * 60)
print(df.isnull().sum())

print("\n" + "=" * 60)
print("DUPLICIDADES")
print("=" * 60)

duplicados = df.duplicated().sum()
print(f"Linhas duplicadas: {duplicados}")

print("\n" + "=" * 60)
print("TIPOS DE DADOS")
print("=" * 60)
print(df.dtypes)

df["data_pedido"] = pd.to_datetime(
    df["data_pedido"],
    errors="coerce"
)
print(df.dtypes)

datas_invalidas = df["data_pedido"].isnull().sum()
print("\nDatas inválidas:", datas_invalidas)

df["estado"] = df["estado"].str.upper()

print("\nEstados encontrados:")
print(sorted(df["estado"].dropna().unique()))

df["categoria"] = df["categoria"].replace(
    {
        "eletronicos": "Eletrônicos"
    }
)

print("\nCategorias encontradas:")
print(sorted(df["categoria"].dropna().unique()))

df["forma_pagamento"] = df["forma_pagamento"].fillna(
    "Não informado"
)

df["faturamento"] = (
    df["quantidade"]
    * df["preco_unitario"]
    * (1 - df["desconto"])
)
df["faturamento"] = df["faturamento"].round(2)

df["custo_total"] = (
    df["quantidade"]
    * df["custo_unitario"]
)
df["custo_total"] = df["custo_total"].round(2)


df["lucro"] = (
    df["faturamento"]
    - df["custo_total"]
)
df["lucro"] = df["lucro"].round(2)

df["margem_lucro"] = (
    df["lucro"] / df["faturamento"]
)
df["margem_lucro"] = df["margem_lucro"].round(4)

df["ano"] = df["data_pedido"].dt.year
df["mes"] = df["data_pedido"].dt.month
df["nome_mes"] = df["data_pedido"].dt.month_name()

print(df.columns.tolist())

print("\n" + "=" * 60)
print("VALIDAÇÃO APÓS TRATAMENTO")
print("=" * 60)

print("Valores nulos:")
print(df.isnull().sum())

print("\nLinhas duplicadas:")
print(df.duplicated().sum())

print("\nTipos:")
print(df.dtypes)

print("\n" + "=" * 60)
print("VALIDAÇÃO FINANCEIRA")
print("=" * 60)

print("Faturamento total:")
print(df["faturamento"].sum())

print("\nCusto total:")
print(df["custo_total"].sum())

print("\nLucro total:")
print(df["lucro"].sum())

print("\nMargem média:")
print(df["margem_lucro"].mean())


faturamento_negativo = (
    df["faturamento"] < 0
).sum()

print("\nFaturamentos negativos:", faturamento_negativo)


quantidade_invalida = (
    df["quantidade"] <= 0
).sum()

print("Quantidades inválidas:", quantidade_invalida)


precos_invalidos = (
    df["preco_unitario"] <= 0
).sum()

print("Preços inválidos:", precos_invalidos)

arquivo_saida.parent.mkdir(
    parents=True,
    exist_ok=True
)

df.to_csv(
    arquivo_saida,
    index=False,
    encoding="utf-8"
)

print("\n" + "=" * 60)
print("ARQUIVO TRATADO SALVO COM SUCESSO!")
print("=" * 60)

print(f"Arquivo: {arquivo_saida}")

print("\n" + "=" * 60)
print("RESUMO DA QUALIDADE DOS DADOS")
print("=" * 60)

print(f"Total de registros: {len(df)}")
print(f"Total de colunas: {len(df.columns)}")
print(f"Duplicados: {df.duplicated().sum()}")
print(
    f"Valores nulos: {df.isnull().sum().sum()}"
)
print(
    f"Faturamentos negativos: {(df['faturamento'] < 0).sum()}"
)
print(
    f"Quantidades inválidas: {(df['quantidade'] <= 0).sum()}"
)
print(
    f"Preços inválidos: {(df['preco_unitario'] <= 0).sum()}"
)