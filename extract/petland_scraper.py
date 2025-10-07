from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from bs4 import BeautifulSoup
import pandas as pd
import time

def scrape_petland(url):

    gecko_path = r"C:\WebDriver\geckodriver.exe"

    options = webdriver.FirefoxOptions()
    options.add_argument("--headless")

    driver = webdriver.Firefox(service=Service(gecko_path), options=options)
    driver.get(url)

    SCROLL_PAUSE_TIME = 1.5
    scroll_increment = 500  # pixels
    last_height = driver.execute_script("return document.body.scrollHeight")
    current_position = 0

    while True:
        driver.execute_script(f"window.scrollTo(0, {current_position});")
        time.sleep(SCROLL_PAUSE_TIME)
        new_height = driver.execute_script("return document.body.scrollHeight")
        
        if current_position >= new_height:
            break
        
        current_position += scroll_increment

    html = driver.page_source
    driver.quit()

    soup = BeautifulSoup(html, "html.parser")
    lojas_divs = soup.select("div.jet-listing-grid__item")

    lista_lojas = []

    for loja in lojas_divs:
        nome_tag = loja.select_one("h2.elementor-heading-title a")
        nome = nome_tag.get_text(strip=True) if nome_tag else ""

        widget_divs = loja.select("div.elementor-widget-text-editor div")
        endereco = widget_divs[0].get_text(strip=True) if len(widget_divs) >= 1 else ""
        telefone = widget_divs[1].get_text(strip=True) if len(widget_divs) >= 2 else ""

        lista_lojas.append({
            "empresa": "petland",
            "nome": nome,
            "endereco": endereco,
            "bairro": "",
            "cidade": "",  
            "estado": "",
            "cep": ""
        })

    df = pd.DataFrame(lista_lojas)

    return df