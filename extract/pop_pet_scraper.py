from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from bs4 import BeautifulSoup
import pandas as pd
import time
import re

def scrape_pop_pet(url):
    gecko_path = r"C:\WebDriver\geckodriver.exe"  # caminho do geckodriver

    options = webdriver.FirefoxOptions()
    options.add_argument("--headless")

    driver = webdriver.Firefox(service=Service(gecko_path), options=options)
    driver.get(url)
    time.sleep(5)  # espera a página carregar

    html = driver.page_source
    driver.quit()

    soup = BeautifulSoup(html, "html.parser")

    lista_lojas = []

    lojas_divs = soup.select("div.gw-gopf-post")  # cada loja é um div com essa classe
    for loja in lojas_divs:
        # Nome da loja
        nome_tag = loja.select_one("div.gw-gopf-post-title h2")
        nome = nome_tag.get_text(strip=True) if nome_tag else ""

        # CEP
        cep_tag = loja.select_one("span.selectable-text.copyable-text")
        cep = cep_tag.get_text(strip=True) if cep_tag else ""

        # Captura link "Ver no Mapa" e extrai latitude/longitude
        link_mapa_tag = loja.find("a", string=re.compile(r"Ver no Mapa"))
        latitude = longitude = ""
        if link_mapa_tag and "href" in link_mapa_tag.attrs:
            href = link_mapa_tag["href"]
            match = re.search(r"@(-?\d+\.\d+),(-?\d+\.\d+),", href)
            if match:
                latitude = match.group(1)
                longitude = match.group(2)

        lista_lojas.append({
            "empresa": "pop pet",
            "nome": nome,
            "endereco": "",
            "bairro": "",
            "cidade": "",
            "estado": "",
            "cep": cep,
            "latitude": latitude,
            "longitude": longitude
        })

    df = pd.DataFrame(lista_lojas)
    df.to_csv("pop_pet_lojas.csv", index=False, encoding="utf-8-sig")
    print(f"{len(df)} lojas salvas em pop_pet_lojas.csv")
    return df
