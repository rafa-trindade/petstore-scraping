from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from bs4 import BeautifulSoup
import pandas as pd
import time
import re

from extract.utils import dados_por_latlong

def scrape_petcamp(url):
    gecko_path = r"C:\WebDriver\geckodriver.exe"

    options = webdriver.FirefoxOptions()
    options.add_argument("--headless")

    driver = webdriver.Firefox(service=Service(gecko_path), options=options)
    driver.get(url)
    time.sleep(5)

    html = driver.page_source
    driver.quit()

    soup = BeautifulSoup(html, "html.parser")

    lista_lojas = []

    # Cada loja está dentro de um container específico
    lojas_divs = soup.select("div.store")  # Ajuste caso necessário

    for loja in lojas_divs:
        nome_tag = loja.select_one("span.name")
        nome = nome_tag.get_text(strip=True) if nome_tag else ""

        endereco_tag = loja.select_one("span.address")
        endereco = endereco_tag.get_text(strip=True) if endereco_tag else ""

        cidade_tag = loja.select_one("span.city")
        cidade = cidade_tag.get_text(strip=True) if cidade_tag else ""

        estado_tag = loja.select_one("span.state")
        estado = estado_tag.get_text(strip=True) if estado_tag else ""

        cep_tag = loja.select_one("span.store-cep")
        cep = cep_tag.get_text(strip=True) if cep_tag else ""

        link_mapa_tag = loja.find("a", href=re.compile(r"google.com/maps/search"))
        latitude = longitude = ""
        if link_mapa_tag and "href" in link_mapa_tag.attrs:
            href = link_mapa_tag["href"]
            match = re.search(r"query=(-?\d+\.\d+),(-?\d+\.\d+)", href)
            if match:
                latitude = match.group(1)
                longitude = match.group(2)

        lista_lojas.append({
            "empresa": "PetCamp",
            "nome": nome,
            "endereco": endereco,
            "bairro": "",
            "cidade": cidade,
            "estado": estado,
            "cep": cep,
            "latitude": latitude,
            "longitude": longitude
        })

    df = pd.DataFrame(lista_lojas)
    df.to_csv("petcamp_lojas.csv", index=False, encoding="utf-8-sig")
    print(f"\n{len(df)} lojas encontradas\n")

    df = dados_por_latlong(df)

    return df
