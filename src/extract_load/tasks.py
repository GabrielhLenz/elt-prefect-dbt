from io import StringIO
from prefect import task
import pandas as pd
import requests
from utils import log
from sqlalchemy import create_engine
from datetime import datetime, timedelta

# Para facilitar a replicabilidade do código, não criei um arquivo .env e disponibilizei a URI direta
DB_URI = "postgresql://postgres:postgres@localhost:5432/postgres"

# Link base da API
API_BASE_URL = "https://brasilapi.com.br/api/cambio/v1"

@task
def download_moedas() -> pd.DataFrame:
    """
    Vamos baixar as moedas listadas pela API.
    """
    response = requests.get(f"{API_BASE_URL}/moedas")
    df = pd.DataFrame(response.json())
    log("Lista de moedas baixada com sucesso!")
    return df

@task
def download_taxas_cambio(simbolo: pd.DataFrame, days = 100) -> pd.DataFrame:
    """
    Obtém as taxas de câmbio dos últimos X (default 100) dias para cada moeda.
    """
    end_date = datetime.today()
    start_date = end_date - timedelta(days=days)
    date_range = [start_date + timedelta(days = i) for i in range(days+1)]

    exchange_rates = []
    
    for _, row in simbolo.iterrows():
        symbol = row["simbolo"]
        for date in date_range:
            formatted_date = date.strftime("%Y-%m-%d")
            response = requests.get(f"{API_BASE_URL}/cotacao/{symbol}/{formatted_date}")
            
            if response.status_code == 200:
                log(date)
                log(symbol)
                data = response.json()
                data["data_consulta"] = formatted_date
                cotacao_fechamento = next((c for c in data["cotacoes"] if c["tipo_boletim"] == "FECHAMENTO PTAX"), None)
                dados_reorganizados = {
                "moeda": data["moeda"],
                "data": data["data"],
                **cotacao_fechamento  # Espalha os dados da cotação diretamente no dicionário
                }
                exchange_rates.append(dados_reorganizados)

    df = pd.DataFrame(exchange_rates)
    log("Taxas de câmbio baixadas com sucesso!")
    return df

@task
def save_csv(dataframe: pd.DataFrame, filename: str) -> None:
    """
    Salva os dados em um arquivo CSV.
    """
    dataframe.to_csv(filename, index=False)
    log(f"Dados salvos em {filename}")

@task
def save_db(dataframe: pd.DataFrame, filename: str, schema = 'extracao') -> None:
    """
    Salva os dados no banco de dados PostgreSQL.
    """
    engine = create_engine(DB_URI)
    dataframe.to_sql(filename, con=engine, schema=schema, if_exists='replace', index=False)
    log("Dados salvos no banco de dados!")
