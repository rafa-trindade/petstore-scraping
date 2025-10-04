from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from bs4 import BeautifulSoup
import pandas as pd
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

        nome_tag = soup.select_one("h3.shop__title")
        nome = nome_tag.get_text(strip=True) if nome_tag else ""

        endereco = ""
        endereco_tag = soup.find("p", string=lambda t: t and "Endereço" in t)
        if endereco_tag:
            endereco_info = endereco_tag.find_next_sibling("p")
            endereco = endereco_info.get_text(strip=True) if endereco_info else ""

        telefone = ""
        tel_tag = soup.find("p", string=lambda t: t and "Telefone" in t)
        if tel_tag:
            tel_info = tel_tag.find_next_sibling("p")
            telefone = tel_info.get_text(strip=True) if tel_info else ""

        horarios = []
        horarios_block = soup.find("p", string=lambda t: t and "Horário" in t)
        if horarios_block:
            horarios_div = horarios_block.find_parent("div", class_="shop__info")
            if horarios_div:
                horarios_tags = horarios_div.find_all("p", class_="shop__info__text")
                horarios = [h.get_text(strip=True) for h in horarios_tags]
        horario_funcionamento = " | ".join(horarios)

        servicos_li = soup.select("ul.shop__services li span")
        servicos_disponiveis = ", ".join([s.get_text(strip=True) for s in servicos_li]) if servicos_li else ""

        key = (nome.strip(), endereco.strip())
        if key in processed_keys:
            return None
        processed_keys.add(key)

        print(f"  + [{idx}] {nome}")

        return {
            "empresa": "petlove",
            "franquia": 1,
            "nome": nome,
            "endereco": endereco,
            "telefone": telefone,
            "horario_funcionamento": horario_funcionamento,
            "servicos_disponiveis": servicos_disponiveis
        }

    cards_inicial = driver.find_elements(By.CSS_SELECTOR, "div.shop__card")
    print(f"Coletando lojas do grupo inicial já expandido ({len(cards_inicial)} cards encontrados).")

    for card in cards_inicial:
        if not card.is_displayed():
            continue
        try:
            loja = process_card(card, 0)
            if loja:
                lista_lojas.append(loja)
        except StaleElementReferenceException:
            continue

    accordions = driver.find_elements(By.CSS_SELECTOR, "div.shops__accordion")
    n_groups = len(accordions)
    print(f"Encontrados {n_groups} grupos (accordions) na página.")

    for idx in range(1, n_groups):  # começa em 1 porque já processamos o primeiro
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

            print(f"Grupo {idx+1}/{n_groups} — lojas coletadas neste grupo: {collected_in_group}")

        except Exception as e:
            print(f"Erro processando grupo {idx+1}: {e}")
            continue

    driver.quit()

    print(f"Total bruto de entradas coletadas: {len(lista_lojas)}")

    df = pd.DataFrame(lista_lojas)
    if df.empty:
        print("⚠️ Nenhuma loja foi coletada.")
    else:
        df_final = df.groupby(["nome", "endereco"], as_index=False).agg({
            "empresa": "first",
            "franquia": "first",
            "telefone": "first",
            "horario_funcionamento": lambda x: " | ".join([v for v in x if v]),
            "servicos_disponiveis": lambda x: ", ".join(sorted(set(", ".join([v for v in x if v]).split(", "))))
        })

        colunas_ordenadas = [
            "empresa",
            "franquia",
            "nome",
            "endereco",
            "telefone",
            "horario_funcionamento",
            "servicos_disponiveis"
        ]
        df = df_final[colunas_ordenadas]

        return df