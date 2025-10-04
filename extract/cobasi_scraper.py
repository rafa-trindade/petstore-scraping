from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import re
import time

def scrape_cobasi(url):

    gecko_path = r"C:\WebDriver\geckodriver.exe"
    driver = webdriver.Firefox(service=Service(gecko_path))

    BASE_URL = url
    driver.get(BASE_URL)

    lista_lojas = []

    while True:
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "storeItem_list_card_item_content__ObdCj"))
        )

        divs = driver.find_elements(By.CLASS_NAME, "storeItem_list_card_item_content__ObdCj")
        
        for div in divs:
            try:
                nome = div.find_element(By.CLASS_NAME, "storeItem_name__gYFCv").text
                p_text = div.find_element(By.TAG_NAME, "p").get_attribute("innerHTML")
                
                p_text = p_text.replace("<br>", "\n")
                lines = p_text.split("\n")
                
                # Endereço e número
                endereco_total = lines[0].strip()
                if "," in endereco_total:
                    endereco, numero = [x.strip() for x in endereco_total.split(",", 1)]
                else:
                    endereco = endereco_total
                    numero = ""
                
                cidade_estado = lines[1].strip()
                if "-" in cidade_estado:
                    cidade, estado = [x.strip() for x in cidade_estado.split("-", 1)]
                else:
                    cidade = cidade_estado
                    estado = ""
                
                cep_match = re.search(r"\d{5}-\d{3}", lines[2])
                cep = cep_match.group() if cep_match else None
                
                lista_lojas.append({
                    "empresa": "cobasi",
                    "nome": nome,
                    "endereco": endereco,
                    "cidade": cidade,
                    "bairro": "",
                    "estado": estado,
                    "cep": cep
                })
            except:
                continue

        try:
            next_btn = driver.find_element(By.CSS_SELECTOR, "button[data-testid='Next page']")
            if "disabled" in next_btn.get_attribute("class"):
                break
            next_btn.click()
            time.sleep(2)
        except:
            break

    driver.quit()

    df = pd.DataFrame(lista_lojas)

    return df


