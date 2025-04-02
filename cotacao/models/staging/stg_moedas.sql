with source as (
    select
        "simbolo",
        "nome"
    from 
        {{ source ('postgres', 'moedas') }}
)

select * from source