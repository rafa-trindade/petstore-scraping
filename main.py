import os
import pandas as pd

from extract.petz_scraper import scrape_petz
from extract.cobasi_scraper import scrape_cobasi
from extract.petlove_scraper import scrape_petlove
from extract.petland_scraper import scrape_petland

BRONZE_DIR = os.path.join("data", "bronze")
os.makedirs(BRONZE_DIR, exist_ok=True)

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
    
    df_final = pd.concat([df_petz, df_cobasi, df_petlove, df_petland], ignore_index=True)
    df_final.to_csv("data/bronze/lojas_bronze.csv", index=False, sep=";", encoding="utf-8-sig")
    print(f"{len(df_final)} lojas salvas em data/bronze/lojas_bronze.csv")


if __name__ == "__main__":
    main()