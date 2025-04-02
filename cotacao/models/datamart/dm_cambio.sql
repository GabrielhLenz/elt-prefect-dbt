
with cambio as(
    select
        moeda,
        data,
        cotacao_venda,
        cotacao_compra
    from
        {{ ref('stg_cambio') }}
),

transacao as(
    select
        data,
        moeda,
        acao,
        quantidade
    from
        {{ ref('stg_dados_transacoes') }}

),

moedas as(
    select
        simbolo,
        nome
    from
        {{ ref('stg_moedas') }}
),

joined as(
    select
        moedas.nome,
        moedas.simbolo,
        cambio.data,
        cambio.cotacao_venda,
        cambio.cotacao_compra,
        transacao.acao,
        transacao.quantidade,
        case
            when transacao.acao = 'venda' then (transacao.quantidade * cambio.cotacao_venda)
            else -(transacao.quantidade * cambio.cotacao_compra)
        end as receita
        from cambio
        inner join
            transacao
        on
            cambio.data = transacao.data
            and cambio.moeda = transacao.moeda
        left join moedas on transacao.moeda = moedas.simbolo
)

select * from joined
