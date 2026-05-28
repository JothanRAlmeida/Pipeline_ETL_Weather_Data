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