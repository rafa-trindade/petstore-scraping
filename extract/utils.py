import os
import pandas as pd
import requests
from tqdm import tqdm
from dotenv import load_dotenv


load_dotenv()

API_TOKEN = os.getenv("API_TOKEN")
HEADERS = {"Authorization": f"Token {API_TOKEN}"}


def dados_por_latlong(df: pd.DataFrame) -> pd.DataFrame:
    url = "https://www.cepaberto.com/api/v3/nearest"

    for col in ['endereco', 'bairro', 'cidade', 'estado', 'cep']:
        if col not in df.columns:
            df[col] = None

    for idx, row in tqdm(df.iterrows(), total=len(df), desc="Preenchendo Campos Ausentes"):
        lat = row.get('latitude')
        lng = row.get('longitude')

        if lat is None or lng is None:
            continue
        try:
            lat = float(lat)
            lng = float(lng)
        except (ValueError, TypeError):
            continue

        params = {'lat': lat, 'lng': lng}
        try:
            response = requests.get(url, headers=HEADERS, params=params, timeout=5)
            if response.status_code == 200:
                data = response.json()

                if data.get('logradouro'):
                    df.at[idx, 'endereco'] = data['logradouro']
                if data.get('bairro'):
                    df.at[idx, 'bairro'] = data['bairro']

                cidade_info = data.get('cidade')
                if cidade_info and cidade_info.get('nome'):
                    df.at[idx, 'cidade'] = cidade_info['nome']

                estado_info = data.get('estado')
                if estado_info and estado_info.get('sigla'):
                    df.at[idx, 'estado'] = estado_info['sigla']

                if data.get('cep'):
                    df.at[idx, 'cep'] = data['cep']

        except Exception as e:
            print(f"⚠️ Erro na linha {idx}: {e}")
            continue

    return df
