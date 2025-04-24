# Modulo para controlar o navegador web
from selenium import webdriver

# localizador de elementos
from selenium.webdriver.common.by import By

# serviço para configurar o caminho de executavel chromedriver
from selenium.webdriver.chrome.service import Service

# classe que permite executar ações avanças(o mover do mouse, clique/arrastar)
from selenium.webdriver.common.action_chains import ActionChains

# classe que espera de forma explicita até que uma condição seja satisfeita
from selenium.webdriver.support.ui import WebDriverWait

# condições esperadas usadas com WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

import pandas as pd

import time

from selenium.common.exceptions import TimeoutException

caminho_driver = "C:\Program Files\chromedriver-win64\chromedriver-win64\chromedriver.exe"

service = Service(caminho_driver)
options = webdriver.ChromeOptions()
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")

driver = webdriver.Chrome(service=service, options=options)

url_base = "https://www.kabum.com.br/hardware/processadores"
driver.get(url_base)
time.sleep(5)

dic_produtos = {"titulo":[], 
                "preco_atual":[],
                "preco_anterior":[], 
                "em_estoque":[]
                }

pagina = 1

while True:
    try:
        WebDriverWait(driver, 10).until(
            ec.presence_of_all_elements_located((By.CLASS_NAME, "productCard"))
        )
    except TimeoutException:
        print("Tempo de espera excedido!")
    
    produtos = driver.find_elements(By.CLASS_NAME, "productCard")
    
    for produto in produtos:
        try:
            titulo = produto.find_element(By.CLASS_NAME, 'nameCard').text.strip()
            preco_original = produto.find_element(By.CLASS_NAME, 'oldPriceCard').text.strip()
            preco_desconto = produto.find_element(By.CLASS_NAME, 'priceCard').text.strip()
            em_estoque = produto.find_element(By.CSS_SELECTOR, 'span.text-xxs.font-semibold.text-black-800').text.strip()
            
            print(f"{titulo} - {preco_original} - {preco_desconto} - {em_estoque}")
            
            dic_produtos["titulo"].append(titulo)
            dic_produtos["preco_atual"].append(preco_desconto)
            dic_produtos["preco_anterior"].append(preco_original)
            dic_produtos["em_estoque"].append(em_estoque)
        
        except Exception as e:
            print("Erro ao coleta dados", e)
            break
        
    try:
        botao_proximo = WebDriverWait(driver, 10).until(
             ec.element_to_be_clickable((By.CLASS_NAME, "nextLink"))
         )
        if botao_proximo:
            driver.execute_script("arguments[0].scrollIntoView();", botao_proximo)
            time.sleep(1)
             
             # Clicar no botão
            driver.execute_script("arguments[0].click();", botao_proximo)
            print(f"Indo para a página {pagina}")
            pagina += 1
            time.sleep(5)
             
        else:
            print("Você chegou na última página!")
    except Exception as e:
        print("Erro ao tentar")
        break 

driver.quit()

df = pd.DataFrame(dic_produtos)
df.to_excel("Processadores.xlsx", index=False)

print(f"Arquivo 'Processadores' salvo com sucesso {len(df)} produtos amazaenados")