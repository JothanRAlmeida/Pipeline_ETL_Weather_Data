from sqlalchemy import create_engine, text
from urllib.parse import quote_plus # Codifica strings para que possam ser enviadas com segurança em uma URL
import os # Para interagir diretamente com o sistema operacional 
from pathlib import Path
import pandas as pd
from dotenv import load_dotenv # Para carregar variáveis de ambiente do arquivo .env
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Cria objeto de caminho para o arquivo .env onde estão as variáveis de ambiente
# resolve() converte um caminho relativo em um caminho absoluto e elimina ambiguidade
env_path = Path(__file__).resolve().parent.parent / 'config' / '.env'
# Carrega variáveis de ambiente
load_dotenv(env_path)

user = os.getenv('user')
password = os.getenv('senha')
database = os.getenv('database')
host = 'host.docker.internal'
#host = 'localhost'

# Conexão com o banco de dados Postgres
def get_engine():
    logging.info(f"-> Conectando em {host}:5432/{database}\n")

    # Define onde está o banco e conecta ao mesmo
    return create_engine(
        f"postgresql+psycopg2://{user}:{quote_plus(password)}@{host}:5432/{database}"
    )

# Chama a conexão com o banco
engine = get_engine()

# Carrega os dados tratados no banco de dados no Postgres
def load_weather_data(table_name: str, df):
    # Para salvar o DataFrame do pandas diretamente no banco de dados
    df.to_sql(
        name = table_name, # Define o nome da tabela no banco de dados
        con = engine, # Conecta o pandas ao banco de dados
        if_exists = 'append', # Determina o que fazer se a tabela já existir no banco
        index = False # Controla se o índice do DataFrame será salvo no banco ou é ignorado
    )

    logging.info(f"-> Dados carregados com sucesso...\n")

    # Consulta a tabela no banco de dados com pandas
    df_check = pd.read_sql(f"SELECT * FROM {table_name}", con = engine)
    logging.info(f"-> Total de registros na tabela: {len(df_check)}\n")