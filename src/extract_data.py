import requests
import json
from pathlib import Path
import logging

# Para registrar eventos, atividades e erros
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

#url = f'https://api.openweathermap.org/data/2.5/weather?q=Montanha,ES,BR&units=metric&lang=pt_br&appid={api_key}'

def extract_weather_data(url: str)->list:
    response = requests.get(url)
    data = response.json()

    if response.status_code != 200:
        logging.error("Erro na requisição!\n")
        return []
    
    if not data:
        logging.warn("Nenhum dado retornado!\n")
        return []

    output_path = 'data/weather_data.json' # Caminho de salvamento dos dados
    output_dir = Path(output_path).parent # parent para o Python entender que estamos uma pasta acima
    output_dir.mkdir(parents=True, exist_ok=True) # Cria caminho e arquivo se não existir

    with open(output_path, 'w') as file:
        # dump transforma estrutura de dado nativo em texto puro com a sintaxe JSON
        # ident = 4 aceita número inteiro para identar a string e deixar mais legível
        json.dump(data, file, indent=4)

    logging.info(f"Arquivo salvo em {output_path}\n")
    return data