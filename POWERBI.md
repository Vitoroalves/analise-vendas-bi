# Guia — Dashboard Power BI

Guia para montar o dashboard no Power BI Desktop a partir do modelo estrela
já gerado. Este documento não substitui o arquivo `.pbix` (que só pode ser
criado dentro do Power BI Desktop) — é o roteiro para você montar.

## 1. Gerar os arquivos do modelo (se ainda não gerou)

```
python scripts/criar_modelo_estrela.py
```

Isso cria em `data/processed/powerbi/`:

| Arquivo | Papel | Chave |
|---|---|---|
| `fato_vendas.csv` | Fato (uma linha por item vendido) | `id_pedido` |
| `dim_produto.csv` | Dimensão de produto/categoria | `id_produto` |
| `dim_cliente.csv` | Dimensão de cliente | `id_cliente` |
| `dim_localizacao.csv` | Dimensão de estado/região | `id_localizacao` |
| `dim_data.csv` | Calendário completo (2025-01-01 a 2026-06-30) | `data` |

## 2. Importar no Power BI Desktop

1. Abrir o Power BI Desktop → **Obter Dados** → **Texto/CSV**
2. Importar os 5 arquivos de `data/processed/powerbi/`
3. Em cada um, conferir se o tipo de dado ficou correto (datas como Data,
   valores monetários como Decimal, `id_*` como Número Inteiro)

## 3. Criar os relacionamentos (Modelagem → Gerenciar Relacionamentos)

Todos como **um-para-muitos**, saindo da dimensão (lado "1") para a fato
(lado "muitos"):

- `dim_produto[id_produto]` → `fato_vendas[id_produto]`
- `dim_cliente[id_cliente]` → `fato_vendas[id_cliente]`
- `dim_localizacao[id_localizacao]` → `fato_vendas[id_localizacao]`
- `dim_data[data]` → `fato_vendas[data_pedido]`

Depois, clicar em `dim_data` → aba **Ferramentas de Tabela** →
**Marcar como Tabela de Datas**, selecionando a coluna `data`. Isso habilita
as funções de inteligência de tempo do DAX (`TOTALYTD`, `SAMEPERIODLASTYEAR`, etc.).

## 4. Medidas DAX

Criar uma tabela só de medidas (Modelagem → Nova Tabela → `Medidas = {}`) e
adicionar as medidas abaixo nela, para manter organizado.

```DAX
Faturamento Total = SUM(fato_vendas[faturamento])

Custo Total = SUM(fato_vendas[custo_total])

Lucro Total = SUM(fato_vendas[lucro])

Margem % = DIVIDE([Lucro Total], [Faturamento Total])

Pedidos = DISTINCTCOUNT(fato_vendas[id_pedido])

Clientes = DISTINCTCOUNT(fato_vendas[id_cliente])

Ticket Médio = DIVIDE([Faturamento Total], [Pedidos])

Faturamento Mês Anterior =
CALCULATE([Faturamento Total], DATEADD(dim_data[data], -1, MONTH))

Variação Faturamento MoM % =
DIVIDE([Faturamento Total] - [Faturamento Mês Anterior], [Faturamento Mês Anterior])

Faturamento Ano Anterior =
CALCULATE([Faturamento Total], SAMEPERIODLASTYEAR(dim_data[data]))

Faturamento Acumulado no Ano =
TOTALYTD([Faturamento Total], dim_data[data])
```

## 5. Estrutura sugerida do dashboard (3 páginas)

### Página 1 — Visão Geral
- Cartões: `Faturamento Total`, `Lucro Total`, `Margem %`, `Ticket Médio`,
  `Pedidos`, `Clientes`
- Gráfico de linha: `Faturamento Total` por `dim_data[ano_mes]`
- Gráfico de colunas: `Faturamento Total` por `dim_produto[categoria]`
- Segmentações de dados (slicers): `dim_data[ano]`, `dim_localizacao[regiao]`

### Página 2 — Produtos
- Tabela/matriz: produto × pedidos × faturamento × lucro × margem
- Gráfico de barras horizontais: top 10 produtos por `Faturamento Total`
- Treemap: `Faturamento Total` por `categoria` → `produto`

### Página 3 — Geografia
- Mapa (ou mapa de árvore) por `estado`, tamanho = `Faturamento Total`
- Gráfico de colunas: `Faturamento Total` por `regiao`
- Tabela com `margem %` por região, para comparar rentabilidade

## 6. Publicar/exportar

- Salvar o arquivo como `powerbi/dashboard_vendas.pbix` na raiz do projeto
  (crie a pasta `powerbi/` se não existir)
- Para portfólio: exportar 2-3 telas como imagem (Arquivo → Exportar → PDF,
  depois print das páginas) e linkar no README

## Checklist

- [ ] Arquivos do modelo estrela importados
- [ ] Relacionamentos criados (4 relações, todas 1-para-muitos)
- [ ] `dim_data` marcada como tabela de datas
- [ ] Medidas DAX criadas
- [ ] Página Visão Geral montada
- [ ] Página Produtos montada
- [ ] Página Geografia montada
- [ ] `.pbix` salvo em `powerbi/`
