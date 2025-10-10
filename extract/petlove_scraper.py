from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from bs4 import BeautifulSoup
import pandas as pd
import re
import time


def scrape_petlove(url):

    gecko_path = r"C:\WebDriver\geckodriver.exe"

    options = webdriver.FirefoxOptions()
    driver = webdriver.Firefox(service=Service(gecko_path), options=options)
    wait = WebDriverWait(driver, 15)

    driver.get(url)
    try:
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.shops__accordion")))
    except TimeoutException:
        print("Timeout: accordions não apareceram. Verifique conexão / bloqueio por bot.")
        driver.quit()
        raise SystemExit

    time.sleep(1)

    lista_lojas = []
    processed_keys = set()

    def process_card(card, idx):
        outer = card.get_attribute("outerHTML")
        soup = BeautifulSoup(outer, "html.parser")

        # Captura nome
        nome_tag = soup.select_one("h3.shop__title")
        nome = nome_tag.get_text(strip=True) if nome_tag else ""

        # Captura endereço completo
        endereco_tag = soup.select_one("p.shop__info__text")
        endereco_full = endereco_tag.get_text(strip=True) if endereco_tag else ""

        # Inicializa variáveis
        endereco, bairro, cidade, estado, cep = "", "", "", "", ""

        if endereco_full:
            parts = [p.strip() for p in endereco_full.split(",")]
            if len(parts) >= 1:
                endereco = parts[0]
            if len(parts) >= 2:
                bairro = parts[1]
            if len(parts) >= 3:
                cidade_estado = parts[2]
                if "-" in cidade_estado:
                    cidade, estado = [x.strip() for x in cidade_estado.split("-", 1)]
                else:
                    cidade = cidade_estado
                    estado = ""
            cep_match = re.search(r"\d{5}-\d{3}", endereco_full)
            if cep_match:
                cep = cep_match.group()

        # Mantém verificação de duplicados
        key = (nome.strip(), endereco.strip())
        if key in processed_keys:
            return None
        processed_keys.add(key)

        return {
            "empresa": "petlove",
            "nome": nome,
            "endereco": endereco,
            "bairro": bairro,
            "cidade": cidade,
            "estado": estado,
            "cep": cep
        }

    # Processa cards iniciais
    cards_inicial = driver.find_elements(By.CSS_SELECTOR, "div.shop__card")

    for card in cards_inicial:
        if not card.is_displayed():
            continue
        try:
            loja = process_card(card, 0)
            if loja:
                lista_lojas.append(loja)
        except StaleElementReferenceException:
            continue

    # Processa accordions restantes
    accordions = driver.find_elements(By.CSS_SELECTOR, "div.shops__accordion")
    n_groups = len(accordions)

    for idx in range(1, n_groups):
        try:
            accordions = driver.find_elements(By.CSS_SELECTOR, "div.shops__accordion")
            if idx >= len(accordions):
                continue

            acc = accordions[idx]
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", acc)
            time.sleep(0.35)
            driver.execute_script("arguments[0].click();", acc)
            time.sleep(0.8)

            cards = driver.find_elements(By.CSS_SELECTOR, "div.shop__card")
            collected_in_group = 0
            for card in cards:
                try:
                    if not card.is_displayed():
                        continue
                    loja = process_card(card, idx+1)
                    if loja:
                        lista_lojas.append(loja)
                        collected_in_group += 1
                except StaleElementReferenceException:
                    continue

        except Exception as e:
            print(f"Erro processando grupo {idx+1}: {e}")
            continue

    driver.quit()

    df = pd.DataFrame(lista_lojas)
    if df.empty:
        print("⚠️ Nenhuma loja foi coletada.")
    else:
        # Mantém agrupamento igual ao original, mas adaptando colunas
        df_final = df.groupby(["nome", "endereco"], as_index=False).agg({
            "empresa": "first",
            "bairro": "first",
            "cidade": "first",
            "estado": "first",
            "cep": "first"
        })

        colunas_ordenadas = [
            "empresa",
            "nome",
            "endereco",
            "bairro",
            "cidade",
            "estado",
            "cep"
        ]
        df = df_final[colunas_ordenadas]

        return df
