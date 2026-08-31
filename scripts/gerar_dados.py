import csv
import random
from datetime import datetime, timedelta
from pathlib import Path


# ============================================================
# CONFIGURAÇÕES
# ============================================================

NUM_VENDAS = 10000
SEED = 42

random.seed(SEED)


# ============================================================
# PRODUTOS
# ============================================================

produtos = [
    {
        "produto": "Notebook",
        "categoria": "Eletrônicos",
        "preco_min": 2500,
        "preco_max": 6000,
        "custo_percentual": 0.72,
    },
    {
        "produto": "Monitor",
        "categoria": "Eletrônicos",
        "preco_min": 700,
        "preco_max": 2500,
        "custo_percentual": 0.68,
    },
    {
        "produto": "Smartphone",
        "categoria": "Eletrônicos",
        "preco_min": 1000,
        "preco_max": 5000,
        "custo_percentual": 0.78,
    },
    {
        "produto": "Teclado",
        "categoria": "Eletrônicos",
        "preco_min": 100,
        "preco_max": 800,
        "custo_percentual": 0.60,
    },
    {
        "produto": "Mouse",
        "categoria": "Eletrônicos",
        "preco_min": 80,
        "preco_max": 500,
        "custo_percentual": 0.58,
    },
    {
        "produto": "Headset",
        "categoria": "Eletrônicos",
        "preco_min": 150,
        "preco_max": 900,
        "custo_percentual": 0.62,
    },
    {
        "produto": "Cafeteira",
        "categoria": "Casa",
        "preco_min": 200,
        "preco_max": 1200,
        "custo_percentual": 0.65,
    },
    {
        "produto": "Air Fryer",
        "categoria": "Casa",
        "preco_min": 300,
        "preco_max": 1000,
        "custo_percentual": 0.64,
    },
    {
        "produto": "Aspirador",
        "categoria": "Casa",
        "preco_min": 250,
        "preco_max": 1500,
        "custo_percentual": 0.67,
    },
    {
        "produto": "Liquidificador",
        "categoria": "Casa",
        "preco_min": 120,
        "preco_max": 600,
        "custo_percentual": 0.63,
    },
    {
        "produto": "Cadeira",
        "categoria": "Escritório",
        "preco_min": 500,
        "preco_max": 2500,
        "custo_percentual": 0.70,
    },
    {
        "produto": "Mesa",
        "categoria": "Escritório",
        "preco_min": 400,
        "preco_max": 2000,
        "custo_percentual": 0.68,
    },
    {
        "produto": "Suporte para Monitor",
        "categoria": "Escritório",
        "preco_min": 100,
        "preco_max": 600,
        "custo_percentual": 0.55,
    },
    {
        "produto": "Luminária",
        "categoria": "Escritório",
        "preco_min": 80,
        "preco_max": 400,
        "custo_percentual": 0.52,
    },
    {
        "produto": "Cabo USB",
        "categoria": "Acessórios",
        "preco_min": 20,
        "preco_max": 100,
        "custo_percentual": 0.45,
    },
    {
        "produto": "Hub USB",
        "categoria": "Acessórios",
        "preco_min": 80,
        "preco_max": 300,
        "custo_percentual": 0.55,
    },
    {
        "produto": "Carregador",
        "categoria": "Acessórios",
        "preco_min": 50,
        "preco_max": 250,
        "custo_percentual": 0.50,
    },
]


# ============================================================
# LOCALIZAÇÃO
# ============================================================

estados_regioes = {
    "SP": "Sudeste",
    "MG": "Sudeste",
    "RJ": "Sudeste",
    "ES": "Sudeste",
    "PR": "Sul",
    "SC": "Sul",
    "RS": "Sul",
    "BA": "Nordeste",
    "PE": "Nordeste",
    "CE": "Nordeste",
    "MA": "Nordeste",
    "PB": "Nordeste",
    "RN": "Nordeste",
    "AL": "Nordeste",
    "SE": "Nordeste",
    "PI": "Nordeste",
    "GO": "Centro-Oeste",
    "MT": "Centro-Oeste",
    "MS": "Centro-Oeste",
    "DF": "Centro-Oeste",
    "AM": "Norte",
    "PA": "Norte",
    "RO": "Norte",
    "AC": "Norte",
    "AP": "Norte",
    "RR": "Norte",
    "TO": "Norte",
}


estados = list(estados_regioes.keys())


# ============================================================
# FORMAS DE PAGAMENTO E CANAIS
# ============================================================

formas_pagamento = [
    "Cartão de crédito",
    "Cartão de débito",
    "PIX",
    "Boleto",
]

canais = [
    "Online",
    "Marketplace",
]


# ============================================================
# GERAR CLIENTES
# ============================================================

NUM_CLIENTES = 2500

clientes = [
    f"C{numero:04d}"
    for numero in range(1, NUM_CLIENTES + 1)
]


# ============================================================
# DATA INICIAL E FINAL
# ============================================================

data_inicio = datetime(2025, 1, 1)
data_fim = datetime(2026, 6, 30)

intervalo_dias = (data_fim - data_inicio).days


# ============================================================
# GERAR VENDAS
# ============================================================

vendas = []

for numero in range(1, NUM_VENDAS + 1):

    produto = random.choice(produtos)

    id_pedido = 100000 + numero

    data_pedido = data_inicio + timedelta(
        days=random.randint(0, intervalo_dias)
    )

    id_cliente = random.choice(clientes)

    quantidade = random.choices(
        [1, 2, 3, 4, 5],
        weights=[55, 25, 12, 6, 2],
        k=1,
    )[0]

    preco_unitario = round(
        random.uniform(
            produto["preco_min"],
            produto["preco_max"]
        ),
        2,
    )

    desconto = random.choices(
        [0, 0.05, 0.10, 0.15, 0.20],
        weights=[35, 25, 25, 10, 5],
        k=1,
    )[0]

    custo_unitario = round(
        preco_unitario * produto["custo_percentual"],
        2,
    )

    estado = random.choice(estados)

    regiao = estados_regioes[estado]

    forma_pagamento = random.choice(formas_pagamento)

    canal = random.choice(canais)

    vendas.append(
        {
            "id_pedido": id_pedido,
            "data_pedido": data_pedido.strftime("%Y-%m-%d"),
            "id_cliente": id_cliente,
            "produto": produto["produto"],
            "categoria": produto["categoria"],
            "quantidade": quantidade,
            "preco_unitario": preco_unitario,
            "desconto": desconto,
            "custo_unitario": custo_unitario,
            "estado": estado,
            "regiao": regiao,
            "forma_pagamento": forma_pagamento,
            "canal": canal,
        }
    )


# ============================================================
# INSERIR ALGUNS PROBLEMAS NOS DADOS
# ============================================================

# Valores nulos
for venda in random.sample(vendas, 80):
    venda["forma_pagamento"] = ""


# Estados escritos de forma inconsistente
for venda in random.sample(vendas, 40):
    if venda["estado"] == "MG":
        venda["estado"] = "mg"


# Categorias inconsistentes
for venda in random.sample(vendas, 30):
    if venda["categoria"] == "Eletrônicos":
        venda["categoria"] = "eletronicos"


# ============================================================
# CRIAR ARQUIVO CSV
# ============================================================

pasta_saida = Path("data/raw")
pasta_saida.mkdir(parents=True, exist_ok=True)

arquivo_saida = pasta_saida / "vendas_raw.csv"

colunas = [
    "id_pedido",
    "data_pedido",
    "id_cliente",
    "produto",
    "categoria",
    "quantidade",
    "preco_unitario",
    "desconto",
    "custo_unitario",
    "estado",
    "regiao",
    "forma_pagamento",
    "canal",
]


with open(
    arquivo_saida,
    "w",
    newline="",
    encoding="utf-8",
) as arquivo:

    escritor = csv.DictWriter(
        arquivo,
        fieldnames=colunas,
    )

    escritor.writeheader()
    escritor.writerows(vendas)


print("=" * 50)
print("DATASET GERADO COM SUCESSO!")
print("=" * 50)
print(f"Total de vendas: {len(vendas)}")
print(f"Total de clientes: {len(clientes)}")
print(f"Arquivo: {arquivo_saida}")