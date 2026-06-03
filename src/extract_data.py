import requests
import json
from pathlib import Path # Para manipular caminhos de arquivos e pastas de forma POO
import logging # Para registrar eventos, erros, alertas e informações de funcionamento

# Biblioteca logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def extract_weather_data(url: str)->list:
    response = requests.get(url) # Requisição para extratir os dados da API
    data = response.json() # Lê a resposta e converte nativamente para dicionário ou lista

    if response.status_code != 200: # Verifica se não obteve sucesso
        logging.error("Erro na requisição!\n")
        return []
    
    if not data: # Verifica se não há dados retornados
        logging.warn("Nenhum dado retornado!\n")
        return []

    output_path = 'data/weather_data.json' # Caminho do arquivo de salvamento dos dados
    output_dir = Path(output_path).parent # Cria um objeto de caminho e o parent informa para subir uma hierarquia
    output_dir.mkdir(parents=True, exist_ok=True) # Cria caminho e arquivo se não existir

    with open(output_path, 'w') as file: # Abre o arquivo para salvar os dados

        # dump  - pega uma estrutura de dados do python (como dicionário) e salva como JSON
        # indent = 4 - Identação para ficar mais legível no arquivo
        json.dump(data, file, indent=4)

    logging.info(f"Arquivo salvo em {output_path}\n")
    return data