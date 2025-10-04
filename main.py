import os
import pandas as pd

from extract.petz_scraper import scrape_petz
from extract.cobasi_scraper import scrape_cobasi
from extract.petlove_scraper import scrape_petlove
from extract.petland_scraper import scrape_petland

from transform.data_processing import tratarmento_petz
from transform.data_processing import tratarmento_cobasi
from transform.data_processing import tratarmento_petlove
from transform.data_processing import tratarmento_petland

BRONZE_DIR = os.path.join("data", "bronze")
SILVER_DIR = os.path.join("data", "silver_raw")
os.makedirs(BRONZE_DIR, exist_ok=True)
os.makedirs(SILVER_DIR, exist_ok=True)

def main():
    url = "https://www.petz.com.br/nossas-lojas"
    print("Coletando dados da Petz...")
    df_petz = scrape_petz(url)
    df_petz.to_csv(os.path.join(BRONZE_DIR, "petz_bronze.csv"), index=False, encoding="utf-8-sig", sep=";")
    print(f"{len(df_petz)} lojas salvas em data/bronze/petz_bronze.csv")

    url = "https://www.cobasi.com.br/lojas"
    print("Coletando dados da Cobasi...")
    df_cobasi = scrape_cobasi(url)
    df_cobasi.to_csv(os.path.join(BRONZE_DIR, "cobasi_bronze.csv"), index=False, encoding="utf-8-sig", sep=";")
    print(f"{len(df_cobasi)} lojas salvas em data/bronze/cobasi_bronze.csv")
    
    url = "https://www.petlove.com.br/lojas-fisicas"
    print("Coletando dados da Petlove...")
    df_petlove = scrape_petlove(url)
    df_petlove.to_csv(os.path.join(BRONZE_DIR, "petlove_bronze.csv"), index=False, encoding="utf-8-sig", sep=";")
    print(f"{len(df_petlove)} lojas salvas em data/bronze/petlove_bronze.csv")
    
    url = "https://petlandbrasil.com.br/lojas/"
    print("Coletando dados da Petland...")
    df_petland = scrape_petland(url)
    df_petland.to_csv(os.path.join(BRONZE_DIR, "petland_bronze.csv"), index=False, encoding="utf-8-sig", sep=";")
    print(f"{len(df_petland)} lojas salvas em data/bronze/petland_bronze.csv")
    
    # --------------- Transformação ------------------

    # Petz
    print("Transformando dados da Petz...")
    df_petz_silver = tratarmento_petz(os.path.join(BRONZE_DIR, "petz_bronze.csv"))
    print(f"{len(df_petz_silver)} lojas salvas.")

    # Cobasi
    print("Transformando dados da Cobasi...")
    df_cobasi_silver = tratarmento_cobasi(os.path.join(BRONZE_DIR, "cobasi_bronze.csv"))
    print(f"{len(df_cobasi_silver)} lojas salvas.")

    # Petlove
    print("Transformando dados da Petlove...")
    df_petlove_silver = tratarmento_petlove(os.path.join(BRONZE_DIR, "petlove_bronze.csv"))
    print(f"{len(df_petlove_silver)} lojas salvas.")

    # Petland
    print("Transformando dados da Petland...")
    df_petland_silver = tratarmento_petland(os.path.join(BRONZE_DIR, "petland_bronze.csv"))
    print(f"{len(df_petland_silver)} lojas salvas.")

    df_final = pd.concat([df_petz_silver, df_cobasi_silver, df_petlove_silver, df_petland_silver], ignore_index=True)
    df_final.to_csv("data/silver_raw/lojas_silver_raw.csv", index=False, sep=";", encoding="utf-8-sig")
    print(f"{len(df_final)} lojas salvas em data/silver_raw/lojas_silver_raw.csv")


if __name__ == "__main__":
    main()