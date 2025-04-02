-- import

with source as (
    select
        "moeda",
        "data",
        "paridade_compra",
        "paridade_venda",
        "cotacao_compra",
        "cotacao_venda"
    from 
        {{ source ('postgres', 'cambio') }}
),
-- renamed

renamed as (
    select 
        "moeda",
        cast("data" as date),
        "paridade_compra",
        "paridade_venda",
        "cotacao_compra",
        "cotacao_venda"
    from
        source
)

-- select * from

select * from renamed