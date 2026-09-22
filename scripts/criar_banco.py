import sqlite3
from pathlib import Path

import pandas as pd


# ============================================================
# CONFIGURAÇÕES
# ============================================================

arquivo_entrada = Path("data/processed/vendas_tratadas.csv")
arquivo_banco = Path("data/processed/vendas.db")


# ============================================================
# CARREGAR DADOS TRATADOS
# ============================================================

df = pd.read_csv(arquivo_entrada)

print("=" * 60)
print("CARREGANDO DADOS NO BANCO SQLITE")
print("=" * 60)

print(f"Linhas lidas: {df.shape[0]}")
print(f"Colunas lidas: {df.shape[1]}")


# ============================================================
# CRIAR/RECRIAR BANCO
# ============================================================

arquivo_banco.parent.mkdir(parents=True, exist_ok=True)

conexao = sqlite3.connect(arquivo_banco)

df.to_sql(
    "vendas",
    conexao,
    if_exists="replace",
    index=False,
)

conexao.execute(
    "CREATE INDEX idx_vendas_categoria ON vendas(categoria)"
)
conexao.execute(
    "CREATE INDEX idx_vendas_regiao ON vendas(regiao)"
)
conexao.execute(
    "CREATE INDEX idx_vendas_produto ON vendas(produto)"
)
conexao.execute(
    "CREATE INDEX idx_vendas_ano_mes ON vendas(ano, mes)"
)

conexao.commit()

total_linhas = conexao.execute(
    "SELECT COUNT(*) FROM vendas"
).fetchone()[0]

conexao.close()

print(f"\nTabela 'vendas' criada com {total_linhas} linhas.")
print(f"Banco salvo em: {arquivo_banco}")
