-- Create Dados Gerais Table

create table dados_gerais(
    salario_bruto real,
    salario_liquido real
)

-- Create Despesas Fixas Table

create table despesas_fixas(
    descricao text,
    categoria text,
    valor_total real,
    valor_mensal real,
    status_pag text,
    forma_pagamento text,
    qual_cartao text,
    qtd_meses integer
)

-- Create Despesas Variaveis Table

create table despesas_variaveis(
    descricao text,
    categoria text,
    valor_total real,
    valor_mensal real,
    qual_cartao text,
    parcelas integer,
    parcelas_pagas integer,
    parcelas_restantes integer
)


-- Create categoria table

-- Create cartao table

-- create forma_pag table