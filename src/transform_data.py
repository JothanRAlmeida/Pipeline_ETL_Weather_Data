import pandas as pd
import json
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# '../data/weather_data.json'
path_name = Path(__file__).parent.parent / 'data' / 'weather_data.json'
columns_names_to_drop = ['weather', 'weather_icon', 'sys.type']
columns_names_to_rename = {
        "base": "base",
        "visibility": "visibility",
        "dt": "datetime",
        "timezone": "timezone",
        "id": "city_id", 
        "name": "city_name",
        "cod": "code",
        "coord.lon": "longitude",
        "coord.lat": "latitude",
        "main.temp": "temperature",
        "main.feels_like": "feels_like",
        "main.temp_min": "temp_min",
        "main.temp_max": "temp_max",
        "main.pressure": "pressure",
        "main.humidity": "humidity",
        "main.sea_level": "sea_level",
        "main.grnd_level": "grnd_level",
        "wind.speed": "wind_speed",
        "wind.deg": "wind_deg",
        "wind.gust": "wind_gust",
        "clouds.all": "clouds", 
        "sys.type": "sys_type",                 
        "sys.id": "sys_id",                
        "sys.country": "country",                
        "sys.sunrise": "sunrise",                
        "sys.sunset": "sunset",
        # weather_id, weather_main, weather_description 
}
columns_to_normalize_datime = ['datetime', 'sunrise', 'sunset']


# Cria o dataframe
def create_dataframe(path_name: str) -> pd.DataFrame:
    logging.INFO("-> Criando data frame...\n")

    path = path_name

    if not path.exist():
        raise FileNotFoundError(f"Arquivo não encontrado: {path}\n")

    with open(path) as file:
       data = json.load(file)

    df = pd.json_normalize(data)

    logging.INFO(f"-> Data frame criado com {len(df)} linha(s)\n")

    return df

# Normaliza coluna do dataframe
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

    logging.INFO(f"Coluna 'weather' normalizada - {len(df.columns)} colunas\n")

    return df

# Remove colunas desnecessárias
def drop_columns(df: pd.DataFrame, columns_names: list[str])->pd.DataFrame:
    logging.INFO(f"-> Removendo colunas {columns_names}\n")

    df = df.drop(columns=columns_names)

    logging.INFO(f"-> Colunas removidas - {len(df.columns)} colunas restantes\n")

    return df

# Renomeia colunas
def rename_columns(df: pd.DataFrame, columns_names: dict[str,str])->pd.DataFrame:
    logging.INFO("->Renomeando colunas...\n")

    df = df.rename(columns=columns_names)

    logging.INFO("-> Colunas renomeadas...\n")

    return df

# Normaliza timestamp para datetime
def normalize_datetime_columns(df: pd.DataFrame, columns_names: list[str])->pd.DataFrame:
    logging.INFO(f"-> Normalizando colunas para datime: {columns_names}\n")

    for name in columns_names:
        df[name] = pd.to_datetime(df[name], unit='s', utc=True).dt.tz_convert('America/Sao_Paulo')

    
    logging.INFO("-> Colunas convertidas para datetime\n")

    return df
