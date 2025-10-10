import os
import sys
import pandas as pd

from extract.cobasi_scraper import scrape_cobasi
from extract.pet_camp_scraper import scrape_petcamp
#from extract.petland_scraper import scrape_petland
from extract.petlove_scraper import scrape_petlove
from extract.petz_scraper import scrape_petz
from extract.pop_pet_scraper import scrape_pop_pet

class Logger:
    def __init__(self, filename):
        self.terminal = sys.stdout
        self.log = open(filename, "w", encoding="utf-8")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)
        self.log.flush()

    def flush(self):
        self.terminal.flush()
        self.log.flush()

BRONZE_DIR = os.path.join("data", "bronze")
LOG_DIR = os.path.join("logs")

for folder in [BRONZE_DIR, LOG_DIR]:
    os.makedirs(folder, exist_ok=True)

log_path = os.path.join(LOG_DIR, "log.txt")
sys.stdout = Logger(log_path)
sys.stderr = sys.stdout 

def main():

    print("----------------------------------------------")
    print("- Coletando dados da Cobasi...")
    print("----------------------------------------------")
    url = "https://www.cobasi.com.br/lojas"
    df_cobasi = scrape_cobasi(url)
    df_cobasi.to_csv(os.path.join(BRONZE_DIR, "cobasi_bronze.csv"), index=False, encoding="utf-8-sig", sep=";")
    print(f"- Processo concluído. {len(df_cobasi)} lojas salvas em data/bronze/cobasi_bronze.csv")

    print("\n----------------------------------------------")
    print("- Coletando dados da Petcamp...")
    print("----------------------------------------------")
    url = "https://www.petcamp.com.br/nossas-lojas/s"
    df_pet_camp = scrape_petcamp(url)
    df_pet_camp.to_csv(os.path.join(BRONZE_DIR, "pet_camp_bronze.csv"), index=False, encoding="utf-8-sig", sep=";")
    print(f"\n- Processo concluído. {len(df_pet_camp)} lojas salvas em data/bronze/pet_camp_bronze.csv")

    print("\n----------------------------------------------")
    print("- Coletando dados da Petland...")
    print("----------------------------------------------")
    #url = "https://petlandbrasil.com.br/lojas/"
    df_petland = pd.read_csv(os.path.join(BRONZE_DIR, "petland_bronze.csv"), encoding="utf-8-sig", sep=";")
    #df_petland.to_csv(os.path.join(BRONZE_DIR, "petland_bronze.csv"), index=False, encoding="utf-8-sig", sep=";")
    print(f"- Processo concluído. {len(df_petland)} lojas salvas em data/bronze/petland_bronze.csv")

    print("\n----------------------------------------------")
    print("- Coletando dados da Petlove...")
    print("----------------------------------------------")
    url = "https://www.petlove.com.br/lojas-fisicas"
    df_petlove = scrape_petlove(url)
    df_petlove.to_csv(os.path.join(BRONZE_DIR, "petlove_bronze.csv"), index=False, encoding="utf-8-sig", sep=";")
    print(f"- Processo concluído. {len(df_petlove)} lojas salvas em data/bronze/petlove_bronze.csv")

    print("\n----------------------------------------------")
    print("- Coletando dados da Petz...")
    print("----------------------------------------------")
    url = "https://www.petz.com.br/nossas-lojas"
    df_petz = scrape_petz(url)
    df_petz.to_csv(os.path.join(BRONZE_DIR, "petz_bronze.csv"), index=False, encoding="utf-8-sig", sep=";")
    print(f"- Processo concluído. {len(df_petz)} lojas salvas em data/bronze/petz_bronze.csv")

    print("\n----------------------------------------------")
    print("- Coletando dados da Pop Pet Center...")
    print("----------------------------------------------")
    url = "https://www.redepoppetcenter.com.br/lojas/"
    df_pop_pet = scrape_pop_pet(url)
    df_pop_pet.to_csv(os.path.join(BRONZE_DIR, "pop_pet_bronze.csv"), index=False, encoding="utf-8-sig", sep=";")
    print(f"- Processo concluído. {len(df_pop_pet)} lojas salvas em data/bronze/pop_pet_bronze.csv")


    print("\n----------------------------------------------")
    print("- Unificação de arquivos Bronze...")
    print("----------------------------------------------")
    df_final = pd.concat([df_cobasi, df_pet_camp, df_petland, df_petlove, df_petz, df_pop_pet], ignore_index=True)
    df_final["data_extracao"] = pd.to_datetime(pd.Timestamp.now()).strftime("%d/%m/%Y")
    data_extracao = df_final['data_extracao'].iloc[0]
    df_final.to_csv("data/bronze/lojas_bronze.csv", index=False, sep=";", encoding="utf-8-sig")
    print(f"- Processo concluído. {len(df_final)} lojas salvas em data/bronze/lojas_bronze.csv")
    print(f"- Data da extração: {data_extracao}")

if __name__ == "__main__":
    main()