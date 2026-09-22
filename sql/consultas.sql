-- ============================================================
-- CONSULTAS SQL — ANÁLISE DE VENDAS
-- Banco: data/processed/vendas.db (tabela "vendas")
-- Gerado a partir de: data/processed/vendas_tratadas.csv
-- Executar com: sqlite3 data/processed/vendas.db
-- ============================================================


-- ============================================================
-- INDICADORES GERAIS
-- ============================================================

-- Faturamento, custo e lucro total, margem geral, pedidos, clientes e ticket médio
SELECT
    ROUND(SUM(faturamento), 2) AS faturamento_total,
    ROUND(SUM(custo_total), 2) AS custo_total,
    ROUND(SUM(lucro), 2) AS lucro_total,
    ROUND(SUM(lucro) * 1.0 / SUM(faturamento), 4) AS margem_lucro,
    COUNT(DISTINCT id_pedido) AS total_pedidos,
    COUNT(DISTINCT id_cliente) AS total_clientes,
    ROUND(SUM(faturamento) * 1.0 / COUNT(DISTINCT id_pedido), 2) AS ticket_medio
FROM vendas;


-- ============================================================
-- TOP 10 PRODUTOS MAIS VENDIDOS (por número de pedidos)
-- ============================================================

SELECT
    produto,
    COUNT(*) AS pedidos
FROM vendas
GROUP BY produto
ORDER BY pedidos DESC
LIMIT 10;


-- ============================================================
-- TOP 10 PRODUTOS POR FATURAMENTO
-- ============================================================

SELECT
    produto,
    ROUND(SUM(faturamento), 2) AS faturamento
FROM vendas
GROUP BY produto
ORDER BY faturamento DESC
LIMIT 10;


-- ============================================================
-- TOP 10 PRODUTOS POR LUCRO
-- ============================================================

SELECT
    produto,
    ROUND(SUM(lucro), 2) AS lucro
FROM vendas
GROUP BY produto
ORDER BY lucro DESC
LIMIT 10;


-- ============================================================
-- ANÁLISE POR CATEGORIA (pedidos, faturamento, lucro, margem)
-- ============================================================

SELECT
    categoria,
    COUNT(DISTINCT id_pedido) AS pedidos,
    ROUND(SUM(faturamento), 2) AS faturamento,
    ROUND(SUM(lucro), 2) AS lucro,
    SUM(quantidade) AS quantidade,
    ROUND(SUM(lucro) * 1.0 / SUM(faturamento), 4) AS margem
FROM vendas
GROUP BY categoria
ORDER BY faturamento DESC;


-- ============================================================
-- ANÁLISE POR REGIÃO (pedidos, faturamento, lucro, margem)
-- ============================================================

SELECT
    regiao,
    COUNT(DISTINCT id_pedido) AS pedidos,
    ROUND(SUM(faturamento), 2) AS faturamento,
    ROUND(SUM(lucro), 2) AS lucro,
    SUM(quantidade) AS quantidade,
    ROUND(SUM(lucro) * 1.0 / SUM(faturamento), 4) AS margem
FROM vendas
GROUP BY regiao
ORDER BY faturamento DESC;


-- ============================================================
-- TOP 10 ESTADOS POR FATURAMENTO
-- ============================================================

SELECT
    estado,
    COUNT(DISTINCT id_pedido) AS pedidos,
    ROUND(SUM(faturamento), 2) AS faturamento,
    ROUND(SUM(lucro), 2) AS lucro
FROM vendas
GROUP BY estado
ORDER BY faturamento DESC
LIMIT 10;


-- ============================================================
-- VENDAS POR MÊS (ano/mês)
-- ============================================================

SELECT
    ano,
    mes,
    COUNT(DISTINCT id_pedido) AS pedidos,
    ROUND(SUM(faturamento), 2) AS faturamento,
    ROUND(SUM(lucro), 2) AS lucro
FROM vendas
GROUP BY ano, mes
ORDER BY ano, mes;


-- ============================================================
-- FATURAMENTO POR ANO
-- ============================================================

SELECT
    ano,
    ROUND(SUM(faturamento), 2) AS faturamento
FROM vendas
GROUP BY ano
ORDER BY ano;


-- ============================================================
-- FATURAMENTO POR MÊS (agregando todos os anos)
-- ============================================================

SELECT
    mes,
    ROUND(SUM(faturamento), 2) AS faturamento
FROM vendas
GROUP BY mes
ORDER BY mes;


-- ============================================================
-- PRODUTOS COM MAIOR MARGEM DE LUCRO
-- ============================================================

SELECT
    produto,
    ROUND(SUM(faturamento), 2) AS faturamento,
    ROUND(SUM(lucro), 2) AS lucro,
    ROUND(SUM(lucro) * 1.0 / SUM(faturamento), 4) AS margem
FROM vendas
GROUP BY produto
ORDER BY margem DESC;


-- ============================================================
-- RESUMO DOS PRODUTOS (pedidos, unidades, faturamento, lucro, margem)
-- ============================================================

SELECT
    produto,
    COUNT(DISTINCT id_pedido) AS pedidos,
    SUM(quantidade) AS unidades,
    ROUND(SUM(faturamento), 2) AS faturamento,
    ROUND(SUM(lucro), 2) AS lucro,
    ROUND(SUM(lucro) * 1.0 / SUM(faturamento), 4) AS margem
FROM vendas
GROUP BY produto
ORDER BY faturamento DESC;


-- ============================================================
-- PRODUTO, CATEGORIA E REGIÃO COM MAIOR FATURAMENTO/LUCRO
-- ============================================================

-- Produto com maior faturamento
SELECT produto, ROUND(SUM(faturamento), 2) AS faturamento
FROM vendas
GROUP BY produto
ORDER BY faturamento DESC
LIMIT 1;

-- Produto com maior lucro
SELECT produto, ROUND(SUM(lucro), 2) AS lucro
FROM vendas
GROUP BY produto
ORDER BY lucro DESC
LIMIT 1;

-- Categoria com maior faturamento
SELECT categoria, ROUND(SUM(faturamento), 2) AS faturamento
FROM vendas
GROUP BY categoria
ORDER BY faturamento DESC
LIMIT 1;

-- Categoria com maior lucro
SELECT categoria, ROUND(SUM(lucro), 2) AS lucro
FROM vendas
GROUP BY categoria
ORDER BY lucro DESC
LIMIT 1;

-- Região com maior faturamento
SELECT regiao, ROUND(SUM(faturamento), 2) AS faturamento
FROM vendas
GROUP BY regiao
ORDER BY faturamento DESC
LIMIT 1;
