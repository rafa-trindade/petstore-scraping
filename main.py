import os
import pandas as pd

from extract.petz_scraper import scrape_petz
from extract.petlove_scraper import scrape_petlove
from extract.petland_scraper import scrape_petland

from transform.data_processing import tratarmento_petz
from transform.data_processing import tratarmento_petlove
from transform.data_processing import tratarmento_petland

BRONZE_DIR = os.path.join("data", "bronze")
SILVER_DIR = os.path.join("data", "silver")
os.makedirs(BRONZE_DIR, exist_ok=True)
os.makedirs(SILVER_DIR, exist_ok=True)

def main():
    url = "https://www.petz.com.br/nossas-lojas"
    print("Coletando dados da Petz...")
    df_petz = scrape_petz(url)
    df_petz.to_csv(os.path.join(BRONZE_DIR, "petz_bronze.csv"), index=False, encoding="utf-8-sig", sep=";")
    print(f"{len(df_petz)} lojas salvas em data/bronze/petz_bronze.csv")

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
    df_petz_silver.to_csv(os.path.join(SILVER_DIR, "petz_silver.csv"),
                            index=False, encoding="utf-8-sig", sep=";")
    print(f"{len(df_petz_silver)} lojas salvas em data/silver/petz_silver.csv")

    # Petlove
    print("Transformando dados da Petlove...")
    df_petlove_silver = tratarmento_petlove(os.path.join(BRONZE_DIR, "petlove_bronze.csv"))
    df_petlove_silver.to_csv(os.path.join(SILVER_DIR, "petlove_silver.csv"),
                                index=False, encoding="utf-8-sig", sep=";")
    print(f"{len(df_petlove_silver)} lojas salvas em data/silver/petlove_silver.csv")

    # Petland
    print("Transformando dados da Petland...")
    df_petland_silver = tratarmento_petland(os.path.join(BRONZE_DIR, "petland_bronze.csv"))
    df_petland_silver.to_csv(os.path.join(SILVER_DIR, "petland_silver.csv"),
                                index=False, encoding="utf-8-sig", sep=";")
    print(f"{len(df_petland_silver)} lojas salvas em data/silver/petland_silver.csv")



if __name__ == "__main__":
    main()