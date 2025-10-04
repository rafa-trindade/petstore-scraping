import pandas as pd
from transform.utils import desmembrar_endereco_petlove, desmembrar_endereco_petland

def tratarmento_petz(csv_path):

  df_petz = pd.read_csv(csv_path, sep=";", encoding="utf-8-sig")
  df_petz["endereco"] = df_petz["endereco"].str.replace(r"[\d,\-\n]+", " ", regex=True).str.replace(r"\s+", " ", regex=True).str.strip()
  df_petz["telefone"] = df_petz["telefone"].str.replace("\n", " ", regex=False).str.replace(r"\s+", " ", regex=True).str.strip()
  
  return df_petz

def tratarmento_petlove(csv_path):

    df_petlove = pd.read_csv(csv_path, sep=";", encoding="utf-8-sig")
    df_petlove["telefone"] = df_petlove["telefone"].str.replace("\n", " ", regex=False).str.replace(r"\s+", " ", regex=True).str.strip()
    df_petlove[["endereco_desmembrado", "bairro", "cidade", "estado", "cep"]] = df_petlove["endereco"].apply(desmembrar_endereco_petlove)
    df_petlove["endereco_desmembrado"] = df_petlove["endereco_desmembrado"].str.replace(r"[\d,-]+", " ", regex=True).str.replace(r"\s+", " ", regex=True).str.replace("\n", " ", regex=False).str.strip()
    df_petlove = df_petlove.drop(columns=["endereco"])
    df_petlove = df_petlove.rename(columns={"endereco_desmembrado": "endereco"})
    
    return df_petlove

def tratarmento_petland(csv_path):

  df_petland = pd.read_csv(csv_path, sep=";", encoding="utf-8-sig")
  df_petland["telefone"] = df_petland["telefone"].str.replace("\n", " ", regex=False).str.replace(r"\s+", " ", regex=True).str.strip()
  df_petland[["endereco_desmembrado", "bairro", "cidade", "estado", "cep"]] = df_petland["endereco"].apply(desmembrar_endereco_petland)
  df_petland["endereco_desmembrado"] = df_petland["endereco_desmembrado"].str.replace(r"[\d,-]+", " ", regex=True).str.replace(r"\s+", " ", regex=True).str.replace("\n", " ", regex=False).str.strip()
  df_petland = df_petland.drop(columns=["endereco"])
  df_petland = df_petland.rename(columns={"endereco_desmembrado": "endereco"})

  return df_petland











