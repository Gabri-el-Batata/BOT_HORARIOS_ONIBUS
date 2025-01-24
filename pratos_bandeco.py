from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time

def configurar_driver(chrome_driver_path: str, chrome_path: str) -> webdriver.Chrome:
    """
    Configura e retorna o driver do Selenium com as opções especificadas.
    """
    chrome_options = Options()
    chrome_options.binary_location = chrome_path
    chrome_options.add_argument("window-size=800,600") 
    service = Service(executable_path=chrome_driver_path)
    return webdriver.Chrome(service=service, options=chrome_options)

def obter_pratos(driver, vegano: bool) -> list:
    """
    Extrai os pratos do site da Prefeitura Unicamp e retorna como uma lista estruturada.
    """
    
    url_extraida = 'https://prefeitura.unicamp.br/cardapio/'
    driver.get(url_extraida)
    time.sleep(0)

    pratos = []
    
    try:
        botao_fecha_cookie_xpath = "/html/body/footer/div[2]/a"
        botao_fecha_cookie = driver.find_element(By.XPATH, botao_fecha_cookie_xpath)
        botao_fecha_cookie.click() 
    except: 
        pass
    
    # Rolar a pagina até os botoes ficarem visiveis (O 600 foi experimental)
    driver.execute_script("window.scrollTo(0, 500)")

    try:
        # Localizando o iframe e mudando o contexto para ele
        iframe = driver.find_element(By.XPATH, "//iframe[@id='cardapio']")
        driver.switch_to.frame(iframe)
        
        ul = driver.find_element(By.XPATH, "/html/body/nav/div/div[2]/ul")
        list_itens = ul.find_elements(By.TAG_NAME, "li")
        num_li = len(list_itens)
        
        time.sleep(2) # Espera coletar informações
        
        
        # Não eh sempre que tem esse botão
        try:
            botao_mostra_dias = driver.find_element(By.XPATH, "/html/body/nav/div/div[1]/button")
            botao_mostra_dias.click()
        except:
            print("Não há botão mostra dias.")
            pass   

        time.sleep(1)

        for i in range(1, num_li+1):
            link = driver.find_element(By.XPATH, f"/html/body/nav/div/div[2]/ul/li[{i}]/a")
            dia = link.text
            print("Recolhendo cardapio de:", dia)

            link.click()

            
            time.sleep(1)
            
            # Encontrando as seções do cardápio
            rows = driver.find_elements(By.CSS_SELECTOR, 'div.row > div')
            for row in rows:
                try:
                    titulo = row.find_element(By.CLASS_NAME, 'menu-section-title').text
                    if ("VEGANO" not in titulo):  # Preferência para excluir menus veganos
                        acompanhamento = row.find_element(By.CSS_SELECTOR, 'div.menu-item-description').text
                        prato_principal = row.find_element(By.CSS_SELECTOR, 'div.menu-item-name').text
                        index_final = acompanhamento.index("Observações")
                        acompanhamento = acompanhamento[:index_final]
                        pratos.append({"dia": dia,
                            "titulo": titulo,
                            "prato_principal": prato_principal,
                            "acompanhamento": acompanhamento
                        })
                except Exception:
                    pass
            try:
                botao_mostra_dias = driver.find_element(By.XPATH, "/html/body/nav/div/div[1]/button")
                botao_mostra_dias.click()
            except:
                print("Não ha botão mostra dias.")
                pass
            time.sleep(2)
    finally:
        driver.quit()

    return pratos

def main() -> list:
    """
    Função principal que configura o driver, extrai os pratos e retorna os resultados.
    """
    # Caminhos do ChromeDriver e do executável do Chrome
    chrome_driver_path = r"C:/Users/gabri/Documents/google_driver/chromedriver.exe"
    chrome_path = r"C:/Users/gabri/Documents/google_driver/chrome-win64/chrome.exe"

    # Configura o driver
    driver = configurar_driver(chrome_driver_path, chrome_path)

    # Obter pratos
    pratos = obter_pratos(driver, True)

    return pratos

nome_arquivo = 'pratos_bandecos.txt'

if __name__ == "__main__":
    resultado = main()
    with open(nome_arquivo, 'w', encoding='utf-8') as arq:
        print("Escrevendo o cardápio extraído no arquivo:", nome_arquivo)
        for prato in resultado:
            arq.write(f"\nDIA: {prato['dia']}")
            arq.write(f"\n{prato['titulo']}")
            arq.write(f"\nPrato principal: {prato['prato_principal']}")
            arq.write(f"\nAcompanhamento: {prato['acompanhamento']}")
