from sqlalchemy import create_engine, text
from urllib.parse import quote_plus
import os
from pathlib import Path
import pandas as pd
from dotenv import load_dotenv
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

env_path = Path(__file__).resolve().parent.parent / 'config' / '.env'
# Carrega variáveis 
load_dotenv(env_path)

user = os.getenv('user')
password = os.getenv('senha')
database = os.getenv('database')
host = 'host.docker.internal'

def get_engine():
    logging.INFO(f"-> Conectando em {host}:5432/{database}\n")

    return create_engine(
        f"postgresql+psycopg2://{user}:{quote_plus(password)}@{host}:5432/{database}"
    )

engine = get_engine()

def load_data(table_name: str, df: pd.DataFrame):
    df.to_sql(
        name = table_name,
        con = engine,
        if_exists = 'append',
        index = False
    )

    logging.INFO(f"-> Dados carregados com sucesso...\n")

    df_check = pd.read_sql(f"SELECT * FROM {database}", con = engine)
    logging.INFO(f"-> Total de registtros na tabela: {len(df_check)}\n")