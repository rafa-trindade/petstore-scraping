import os
import sys
import pandas as pd

from extract.petz_scraper import scrape_petz
from extract.cobasi_scraper import scrape_cobasi

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
    print("- Coletando dados da Petz...")
    print("----------------------------------------------")
    url = "https://www.petz.com.br/nossas-lojas"
    df_petz = scrape_petz(url)
    df_petz.to_csv(os.path.join(BRONZE_DIR, "petz_bronze.csv"), index=False, encoding="utf-8-sig", sep=";")
    print(f"- Processo concluído. {len(df_petz)} lojas salvas em data/bronze/petz_bronze.csv")

    print("\n----------------------------------------------")
    print("- Coletando dados da Cobasi...")
    print("----------------------------------------------")
    url = "https://www.cobasi.com.br/lojas"
    df_cobasi = scrape_cobasi(url)
    df_cobasi.to_csv(os.path.join(BRONZE_DIR, "cobasi_bronze.csv"), index=False, encoding="utf-8-sig", sep=";")
    print(f"- Processo concluído. {len(df_cobasi)} lojas salvas em data/bronze/cobasi_bronze.csv")


    print("\n----------------------------------------------")
    print("- Unificação de arquivos Bronze...")
    print("----------------------------------------------")
    df_final = pd.concat([df_petz, df_cobasi], ignore_index=True)
    df_final["data_extracao"] = pd.to_datetime(pd.Timestamp.now()).strftime("%d/%m/%Y")
    data_extracao = df_final['data_extracao'].iloc[0]
    df_final.to_csv("data/bronze/lojas_bronze.csv", index=False, sep=";", encoding="utf-8-sig")
    print(f"- Processo concluído. {len(df_final)} lojas salvas em data/bronze/lojas_bronze.csv")
    print(f"- Data da extração: {data_extracao}")

if __name__ == "__main__":
    main()