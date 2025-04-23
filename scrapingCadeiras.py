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

# uso de tratamento de exceção
from selenium.common.exceptions import TimeoutException

# definir o caminho do chromedriver
caminho_driver = "C:\Program Files\chromedriver-win64\chromedriver-win64\chromedriver.exe"

# configuração do WebDriver
service = Service(caminho_driver) # Inicializar o navegador
options = webdriver.ChromeOptions() #configurar as opções do navegador
# options.add_argument("--headless") Executa o navegador sem abrir a interface
options.add_argument("--disable-gpu") # evita possíveis erros gráficos
options.add_argument("--window-size=1920,1080") # define uma resolução fixa

# inicialização do WebDriver
driver = webdriver.Chrome(service=service, options=options)

# URL inicial
url_base = "https://www.kabum.com.br/espaco-gamer/cadeiras-gamer"
driver.get(url_base)
time.sleep(5) #aguarda 5 seg para garantir que a pág carregue

# criar um dicionário vazio para armazenar os nomes e precos das cadeiras
dic_produtos = {"marca":[], "preco":[]}

#vamos inciar na pagina 1 e incrementamos a cada trocad de pagina
pagina = 1

while True:
    print(f"\n Coletando dados da página {pagina}...")
    try:
        # Cria uma espera de até 10 seg
        WebDriverWait(driver, 10).until( # faz com que o código espere até que a condição seja verdadeira
            # verifica se todos os elementos "productCard" estão acessíveis
            ec.presence_of_all_elements_located((By.CLASS_NAME, "productCard")) # Indica que a busca será feita através da classe
        )
        print("Elementos encontrados com sucesso!")
    except TimeoutException:
        print("Tempo de espera excedido!")
    
    produtos = driver.find_elements(By.CLASS_NAME,"productCard")
    
    for produto in produtos:
        try:
            nome = produto.find_element(By.CLASS_NAME,"nameCard").text.strip()
            preco = produto.find_element(By.CLASS_NAME,"priceCard").text.strip()
            
            print(f"{nome} - {preco}")
            
            dic_produtos["marca"].append(nome)
            dic_produtos["preco"].append(preco)
            
            
        except Exception:
            print("Erro ao coleta dados", Exception)
            break
    # encontrar o acesso para a proxima pagina
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
     
    # fechar o navegador
driver.quit()
    
    # dataframe
df = pd.DataFrame(dic_produtos)
df.to_excel("cadeiras.xlsx", index=False)
    
print(f"Arquivo 'Cadeiras' salvo com sucesso {len(df)} produtos amazaenados")
    
    # salvar os dados em csv(dataframe)