import os
import pandas as pd

from extract.petz_scraper import scrape_petz
from extract.petlove_scraper import scrape_petlove
from extract.petland_scraper import scrape_petland

from transform.data_processing import tratarmento_petz
from transform.data_processing import tratarmento_petlove
from transform.data_processing import tratarmento_petland

RAW_DIR = os.path.join("data", "raw")
PROCESSED_DIR = os.path.join("data", "processed")
os.makedirs(RAW_DIR, exist_ok=True)
os.makedirs(PROCESSED_DIR, exist_ok=True)

def main():
    url = "https://www.petz.com.br/nossas-lojas"
    print("Coletando dados da Petz...")
    df_petz = scrape_petz(url)
    df_petz.to_csv(os.path.join(RAW_DIR, "petz_raw.csv"), index=False, encoding="utf-8-sig", sep=";")
    print(f"{len(df_petz)} lojas salvas em data/raw/petz_raw.csv")

    url = "https://www.petlove.com.br/lojas-fisicas"
    print("Coletando dados da Petlove...")
    df_petlove = scrape_petlove(url)
    df_petlove.to_csv(os.path.join(RAW_DIR, "petlove_raw.csv"), index=False, encoding="utf-8-sig", sep=";")
    print(f"{len(df_petlove)} lojas salvas em data/raw/petlove_raw.csv")
    
    url = "https://petlandbrasil.com.br/lojas/"
    print("Coletando dados da Petland...")
    df_petland = scrape_petland(url)
    df_petland.to_csv(os.path.join(RAW_DIR, "petland_raw.csv"), index=False, encoding="utf-8-sig", sep=";")
    print(f"{len(df_petland)} lojas salvas em data/raw/petland_raw.csv")
    
    # --------------- Transformação ------------------

    # Petz
    print("Transformando dados da Petz...")
    df_petz_processed = tratarmento_petz(os.path.join(RAW_DIR, "petz_raw.csv"))
    df_petz_processed.to_csv(os.path.join(PROCESSED_DIR, "petz_processed.csv"),
                            index=False, encoding="utf-8-sig", sep=";")
    print(f"{len(df_petz_processed)} lojas salvas em data/processed/petz_processed.csv")

    # Petlove
    print("Transformando dados da Petlove...")
    df_petlove_processed = tratarmento_petlove(os.path.join(RAW_DIR, "petlove_raw.csv"))
    df_petlove_processed.to_csv(os.path.join(PROCESSED_DIR, "petlove_processed.csv"),
                                index=False, encoding="utf-8-sig", sep=";")
    print(f"{len(df_petlove_processed)} lojas salvas em data/processed/petlove_processed.csv")

    # Petland
    print("Transformando dados da Petland...")
    df_petland_processed = tratarmento_petland(os.path.join(RAW_DIR, "petland_raw.csv"))
    df_petland_processed.to_csv(os.path.join(PROCESSED_DIR, "petland_processed.csv"),
                                index=False, encoding="utf-8-sig", sep=";")
    print(f"{len(df_petland_processed)} lojas salvas em data/processed/petland_processed.csv")



if __name__ == "__main__":
    main()