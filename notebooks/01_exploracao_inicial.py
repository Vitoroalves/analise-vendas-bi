import pandas as pd


arquivo = "data/raw/vendas_raw.csv"

df = pd.read_csv(arquivo)


print("Primeiras linhas:")
print(df.head())


print("\nDimensões:")
print(df.shape)


print("\nColunas:")
print(df.columns.tolist())

print("\nInformações do DataFrame:")
print(df.info())

print("\nValores Nulos:")
print(df.isnull().sum())

print("\nEstatísticas:")
print(df.describe())