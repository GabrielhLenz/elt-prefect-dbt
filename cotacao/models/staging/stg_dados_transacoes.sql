with source as(
    select
        *
    from
        {{ source ('postgres', 'dados_transacoes')}}
),

renamed as (
    select 
        cast("data" as date),
        "moeda",
        "acao",
        cast("quantidade" as integer)
    from
        source
)

select * from renamed