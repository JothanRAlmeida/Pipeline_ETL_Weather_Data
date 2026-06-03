from datetime import datetime, timedelta # Para trabalhar com datas, horas e durações
from airflow.decorators import dag, task # Para criar DAGS e tarefas no airflow
from pathlib import Path
import sys # Para iteragir diretamente com o interpretador
import os

# Inclui na primeira posição da lista que contém os diretórios o caminho informado, sendo priorizado
sys.path.insert(0, '/opt/airflow/src')

# Importa as funções criadas no ETL
from extract_data import extract_weather_data
from load_data import load_weather_data
from transform_data import data_transformations
from dotenv import load_dotenv

# Cria objeto de caminho para o arquivo .env onde estão as variáveis de ambiente
env_path = Path(__file__).resolve().parent.parent / 'config' / '.env'
# Carrega variáveis de ambiente
load_dotenv(env_path)

API_KEY = os.getenv('api_key') # Busca a chave API para acessá-la
url = f'https://api.openweathermap.org/data/2.5/weather?q=Montanha,ES,BR&units=metric&lang=pt_br&appid={API_KEY}'

# Fluxo de execução do pipeline - Argumentos
@dag(
    dag_id='weather_pipeline', # Identificador único no ambiente
    default_args={ # Argumentos padrão da DAG
        'owner': 'airflow', # Indica quem é o responsável pela DAG - Apenas informativo
        'depends_on_past': False, # Define se uma execução depende de outra execução anterior
        'retries': 2, # Quantidade de tentativas em caso de erro
        'retry_delay': timedelta(minutes=5) # Tempo de espera entre tentativas
    },
    description='Pipeline ETL - CLima Montanha', # Descrição exibida na interface
    schedule='0 */1 * * * ', # Quando será executada (minuto, hora, dia do mês, mês, dia da semana) - Esse exemplo: A cada 1 hora
    start_date=datetime(2026, 2, 7), # Data a partir de quando o Airflow começa a considerar execuções
    catchup=False, # Controla se o Airflow executará períodos passados que ficaram pendetes
    tags=['weather', 'etl', 'pipeline'] # Para organizar e filtrar DAGs na interface
)

# Define as tarefas que a DAG irá executar
def weather_pipeline():

    @task
    def extract():
        extract_weather_data(url)

    @task
    def transform():
        df = data_transformations()
        # Salva como parquet - Alta performance, economia de espaço e preservação dos tipos de dados
        df.to_parquet('/opt/airflow/data/tempo_data_parquet', index=False) 

    @task
    def load():
        import pandas as pd
        df = pd.read_parquet('/opt/airflow/data/tempo_data_parquet')
        load_weather_data('montanha_weather', df)

    # Ordem de execução das tarefas
    extract() >> transform() >> load()

weather_pipeline()