from pathlib import Path

import pandas as pd


# ============================================================
# CONFIGURAÇÕES
# ============================================================

arquivo_entrada = Path("data/processed/vendas_tratadas.csv")
pasta_saida = Path("data/processed/powerbi")
pasta_saida.mkdir(parents=True, exist_ok=True)

MESES_PT = {
    1: "Janeiro", 2: "Fevereiro", 3: "Março", 4: "Abril",
    5: "Maio", 6: "Junho", 7: "Julho", 8: "Agosto",
    9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro",
}

DIAS_SEMANA_PT = {
    0: "Segunda-feira", 1: "Terça-feira", 2: "Quarta-feira",
    3: "Quinta-feira", 4: "Sexta-feira", 5: "Sábado", 6: "Domingo",
}


# ============================================================
# LEITURA DOS DADOS TRATADOS
# ============================================================

df = pd.read_csv(arquivo_entrada, parse_dates=["data_pedido"])

print("=" * 60)
print("CRIANDO MODELO ESTRELA PARA POWER BI")
print("=" * 60)
print(f"Linhas de origem: {df.shape[0]}")


# ============================================================
# DIM_PRODUTO
# ============================================================

dim_produto = (
    df[["produto", "categoria"]]
    .drop_duplicates()
    .sort_values("produto")
    .reset_index(drop=True)
)
dim_produto.insert(0, "id_produto", range(1, len(dim_produto) + 1))

mapa_produto = dict(
    zip(dim_produto["produto"], dim_produto["id_produto"])
)


# ============================================================
# DIM_LOCALIZACAO
# ============================================================

dim_localizacao = (
    df[["estado", "regiao"]]
    .drop_duplicates()
    .sort_values("estado")
    .reset_index(drop=True)
)
dim_localizacao.insert(
    0, "id_localizacao", range(1, len(dim_localizacao) + 1)
)

mapa_localizacao = dict(
    zip(dim_localizacao["estado"], dim_localizacao["id_localizacao"])
)


# ============================================================
# DIM_CLIENTE
# ============================================================

dim_cliente = (
    df[["id_cliente"]]
    .drop_duplicates()
    .sort_values("id_cliente")
    .reset_index(drop=True)
)


# ============================================================
# DIM_DATA (calendário completo, não só as datas com vendas)
# ============================================================

data_inicio = df["data_pedido"].min()
data_fim = df["data_pedido"].max()

calendario = pd.date_range(data_inicio, data_fim, freq="D")

dim_data = pd.DataFrame({"data": calendario})
dim_data["ano"] = dim_data["data"].dt.year
dim_data["mes"] = dim_data["data"].dt.month
dim_data["nome_mes"] = dim_data["mes"].map(MESES_PT)
dim_data["trimestre"] = dim_data["data"].dt.quarter
dim_data["dia"] = dim_data["data"].dt.day
dim_data["dia_semana"] = dim_data["data"].dt.dayofweek.map(DIAS_SEMANA_PT)
dim_data["fim_de_semana"] = dim_data["data"].dt.dayofweek >= 5
dim_data["ano_mes"] = dim_data["data"].dt.strftime("%Y-%m")


# ============================================================
# FATO_VENDAS
# ============================================================

fato_vendas = df.copy()
fato_vendas["id_produto"] = fato_vendas["produto"].map(mapa_produto)
fato_vendas["id_localizacao"] = fato_vendas["estado"].map(mapa_localizacao)

fato_vendas = fato_vendas[
    [
        "id_pedido",
        "data_pedido",
        "id_cliente",
        "id_produto",
        "id_localizacao",
        "quantidade",
        "preco_unitario",
        "desconto",
        "custo_unitario",
        "forma_pagamento",
        "canal",
        "faturamento",
        "custo_total",
        "lucro",
        "margem_lucro",
    ]
]


# ============================================================
# SALVAR ARQUIVOS (formato compatível com Power BI pt-BR)
# ============================================================

# Configuração para CSV em português: vírgula como decimal, ponto e vírgula como separador
csv_config = {
    "index": False,
    "sep": ";",
    "decimal": ",",
    "encoding": "utf-8-sig"
}

fato_vendas.to_csv(pasta_saida / "fato_vendas.csv", **csv_config)
dim_produto.to_csv(pasta_saida / "dim_produto.csv", **csv_config)
dim_cliente.to_csv(pasta_saida / "dim_cliente.csv", **csv_config)
dim_localizacao.to_csv(pasta_saida / "dim_localizacao.csv", **csv_config)
dim_data.to_csv(pasta_saida / "dim_data.csv", **csv_config)

print(f"\nfato_vendas: {fato_vendas.shape[0]} linhas")
print(f"dim_produto: {dim_produto.shape[0]} linhas")
print(f"dim_cliente: {dim_cliente.shape[0]} linhas")
print(f"dim_localizacao: {dim_localizacao.shape[0]} linhas")
print(f"dim_data: {dim_data.shape[0]} linhas")
print(f"\nArquivos salvos em: {pasta_saida}")
