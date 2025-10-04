from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from bs4 import BeautifulSoup
import pandas as pd
import time

def scrape_petz(url):

    gecko_path = r"C:\WebDriver\geckodriver.exe"

    options = webdriver.FirefoxOptions()
    options.add_argument("--headless")

    driver = webdriver.Firefox(service=Service(gecko_path), options=options)

    driver.get(url)
    time.sleep(5) 

    html = driver.page_source
    driver.quit()

    soup = BeautifulSoup(html, "html.parser")
    lojas_divs = soup.select("div.store")

    lista_lojas = []
    for loja in lojas_divs:
        nome = loja.find(attrs={"itemprop": "name"})
        nome = nome.get_text(strip=True) if nome else ""

        endereco = loja.find(attrs={"itemprop": "streetAddress"})
        endereco = endereco.get_text(strip=True) if endereco else ""

        endereco_span = loja.find("span", {"itemprop": "streetAddress"})
        bairro_span = endereco_span.find_next_sibling("span") if endereco_span else None
        bairro_text = bairro_span.get_text(strip=True) if bairro_span else ""
        bairro = bairro_text.split("-")[0].strip() if "-" in bairro_text else bairro_text

        cidade = loja.find(attrs={"itemprop": "addressLocality"})
        cidade = cidade.get_text(strip=True) if cidade else ""

        estado = loja.find(attrs={"itemprop": "addressRegion"})
        estado = estado.get_text(strip=True) if estado else ""

        cep = loja.find(attrs={"itemprop": "postalCode"})
        cep = cep.get_text(strip=True) if cep else ""

        telefone = loja.find(attrs={"itemprop": "telephone"})
        telefone = telefone.get_text(strip=True) if telefone else ""

        horario_funcionamento = loja.find(attrs={"itemprop": "openingHours"})
        horario_funcionamento = horario_funcionamento.get_text(strip=True) if horario_funcionamento else ""

        produtos_span = loja.select("p[id^='petzCategory'] .caption-text")
        produtos_para = ", ".join([p.get_text(strip=True) for p in produtos_span]) if produtos_span else ""

        servicos_li = loja.select("ul[id^='services'] li")  # seleciona todos os <li> de serviços
        servicos_disponiveis = ", ".join([s.get_text(strip=True) for s in servicos_li]) if servicos_li else ""

        lista_lojas.append({
            "empresa": "petz",
            "nome": nome,
            "endereco": endereco,
            "bairro": bairro,
            "cidade": cidade,
            "estado": estado,
            "cep": cep,
        })

    df = pd.DataFrame(lista_lojas)

    return df 

