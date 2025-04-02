from prefect import Flow, Parameter

from tasks import  download_moedas, download_taxas_cambio, save_csv, save_db

with Flow("cambio") as flow:
    # Definindo um parâmetro para o número de usuários a serem baixados
    days = Parameter("days", default=1)

    # Tasks
    moedas = download_moedas()
    cambio = download_taxas_cambio(moedas, days)
    save_db(moedas, 'moedas')
    save_db(cambio, 'cambio')