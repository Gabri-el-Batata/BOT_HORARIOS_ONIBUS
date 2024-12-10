from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

def configurar_driver(chrome_driver_path, chrome_path):
    """
    Configura e retorna o driver do Selenium com as opções especificadas.
    """
    chrome_options = Options()
    chrome_options.binary_location = chrome_path
    service = Service(executable_path=chrome_driver_path)
    return webdriver.Chrome(service=service, options=chrome_options)

def obter_pratos(driver):
    """
    Extrai os pratos do site da Prefeitura Unicamp e retorna como uma lista estruturada.
    """
    driver.get('https://prefeitura.unicamp.br/cardapio/')
    time.sleep(2)

    pratos = []

    try:
        # Localizando o iframe e mudando o contexto para ele
        iframe = driver.find_element(By.XPATH, "//iframe[@id='cardapio']")
        driver.switch_to.frame(iframe)
        
        ul = driver.find_element(By.XPATH, "/html/body/nav/div/div[2]/ul")
        list_itens = ul.find_elements(By.TAG_NAME, "li")
        num_li = len(list_itens)
        time.sleep(1) # Espera coletar informações
        
        
        botao_mostra_dias = driver.find_element(By.XPATH, "/html/body/nav/div/div[1]/button")
        botao_mostra_dias.click()
        time.sleep(1) # Espera aparecer as informações
        
        #teste = driver.find_element(By.XPATH, "/html/body/nav/div/div[2]/ul/li[3]")
        
        
        
        for i in range(1, num_li+1):
            teste = driver.find_element(By.XPATH, f"/html/body/nav/div/div[2]/ul/li[{i}]/a")
            dia = teste.text

            teste.click()
            
            time.sleep(1)
            
            # Encontrando as seções do cardápio
            rows = driver.find_elements(By.CSS_SELECTOR, 'div.row > div')
            for row in rows:
                try:
                    titulo = row.find_element(By.CLASS_NAME, 'menu-section-title').text
                    if "VEGANO" not in titulo:  # Preferência para excluir menus veganos
                        acompanhamento = row.find_element(By.CSS_SELECTOR, 'div.menu-item-description').text
                        index_final = acompanhamento.index("Observações")
                        acompanhamento = acompanhamento[:index_final]
                        pratos.append({"dia": dia,
                            "titulo": titulo,
                            "prato_principal": row.find_element(By.CSS_SELECTOR, 'div.menu-item-name').text,
                            "acompanhamento": acompanhamento
                        })
                    time.sleep(1)
                except Exception:
                    pass
            time.sleep(1)
            botao_mostra_dias = driver.find_element(By.XPATH, "/html/body/nav/div/div[1]/button")
            botao_mostra_dias.click()
            time.sleep(1)
    finally:
        driver.quit()

    return pratos

def main():
    """
    Função principal que configura o driver, extrai os pratos e retorna os resultados.
    """
    # Caminhos do ChromeDriver e do executável do Chrome
    chrome_driver_path = r"C:/Users/gabri/Documents/google_driver/chromedriver.exe"
    chrome_path = r"C:/Users/gabri/Documents/google_driver/chrome-win64/chrome.exe"

    # Configura o driver
    driver = configurar_driver(chrome_driver_path, chrome_path)

    # Obter pratos
    pratos = obter_pratos(driver)

    return pratos

nome_arquivo = 'pratos_bandecos.txt'

if __name__ == "__main__":
    resultado = main()
    with open(nome_arquivo, 'w', encoding='utf-8') as arq:
        for prato in resultado:
            arq.write(f"\nDIA: {prato['dia']}")
            arq.write(f"\n{prato['titulo']}")
            arq.write(f"\nPrato principal: {prato['prato_principal']}")
            arq.write(f"\nAcompanhamento: {prato['acompanhamento']}")