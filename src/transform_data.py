import pandas as pd
import json
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# '../data/weather_data.json'
path_name = Path(__file__).parent.parent / 'data' / 'weather_data.json'

# Cria o dataframe
def create_dataframe(path_name: str) -> pd.DataFrame:
    logging.INFO("-> Criando data frame...\n")

    path = path_name

    if not path.exist():
        raise FileNotFoundError(f"Arquivo não encontrado: {path}")

    with open(path) as file:
       data = json.load(file)

    df = pd.json_normalize(data)

    logging.INFO(f"-> Data frame criado com {len(df)} linha(s)\n")

    return df

def normalize_dataframe(df: pd.DataFrame)->pd.DataFrame:
    logging.INFO("-> Normalizando o data frame...\n")

    # lambda transforma a lista contendo um dicionário em colunas
    df_weather = pd.json_normalize(df["weather"].apply(lambda x: x[0]))

    # Renomear colunas pois nomes já existem
    df_weather = df_weather.rename(columns={
        "id": "weather_id",
        "main": "weather_main",
        "description": "weather_description",
        "icon": "weather_icon"
    })

    # Concatena as colunas
    df = pd.concat([df, df_weather], axis=1)

    logging.INFO(f"Coluna 'weather' normalizada - {len(df.columns)} colunas")

    return df