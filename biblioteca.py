from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
import time

# Caminho para o ChromeDriver atualizado
chrome_driver_path = r"C:/Users/gabri/Documents/google_driver/chromedriver.exe"

# Caminho para o executável do Chrome
chrome_path = r"C:\Users\gabri\Documents\google_driver\chrome-win64\chrome.exe".replace('\\', '/')  # Atualize com o caminho da versão desejada

# Configuração do Selenium para usar o Chrome com ChromeDriver
chrome_options = Options()
chrome_options.binary_location = chrome_path
chrome_options.add_argument("--headless") 

# Inicialize o driver usando as opções e o serviço configurados
service = Service(executable_path=chrome_driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

# Acesse o Google
driver.get('https://acervus.unicamp.br')
time.sleep(2)

try:
    buttons = driver.find_element(By.CSS_SELECTOR, "li.dropdown.usuarios a[ng-click='openLoginCtrl.abrirPopupLogin()']")
    buttons.click()
    time.sleep(2)

    iframe = driver.find_element(By.CSS_SELECTOR, "#loginWindow > iframe")
    driver.switch_to.frame(iframe)


    email_field = driver.find_element(By.CSS_SELECTOR, "#login-identificacao")  # Substitua o seletor pelo correto
    password_field = driver.find_element(By.CSS_SELECTOR, "#login-senha")

    
    email_field.send_keys("g250311@dac.unicamp.br")
    password_field.send_keys("445216")

    login_submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")  # Substitua o seletor pelo correto
    login_submit_button.click() 

    time.sleep(2)

    driver.switch_to.default_content()

    driver.get('https://acervus.unicamp.br/emprestimo')

    time.sleep(2)

    table = driver.find_element(By.CSS_SELECTOR, '#gridCirculacaoAberta > table')  # Ajuste o seletor conforme necessário
    tbody = table.find_element(By.CSS_SELECTOR, '#gridCirculacaoAberta > table > tbody')

    rows = tbody.find_elements(By.TAG_NAME, 'tr')

    for row in rows:
        cells = row.find_elements(By.TAG_NAME, 'td')
        if len(cells) < 2:
            print("Você não tem empréstimos ativos.")
            break
        nome_livro = cells[2].text.strip()  # Nome do livro está na primeira célula
        data_final = cells[7].text.strip()  # Data final está na sexta célula
        
        # Imprima ou armazene as informações
        print(f'Nome do livro: {nome_livro}')
        print(f'Data prevista: {data_final}')


finally:
    driver.quit()