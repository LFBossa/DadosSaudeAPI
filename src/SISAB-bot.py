# selenium 4
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService

from selenium.webdriver.support.expected_conditions import visibility_of_all_elements_located
from selenium.webdriver.support.wait import WebDriverWait

from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By

from pathlib import Path
from time import sleep

def create_driver(download_path):
    chrome_options = Options()
    chrome_options.add_experimental_option("prefs", {
            "download.default_directory": download_path,
            "download.prompt_for_download": False
    })
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options) 
    return driver

 
URL = "https://sisab.saude.gov.br/paginas/acessoRestrito/relatorio/federal/saude/RelSauProducao.xhtml"


def selecionando_competencia(driver, competência):
    """Clica no botão multiselect e seleciona a competência desejada"""
    botao_competência = driver.find_element(By.CSS_SELECTOR, "#competencia button.multiselect")
    botao_competência.click()
    li = driver.find_element(By.CSS_SELECTOR, f"#competencia input[value='{competência}']")
    li.click()
    botao_competência.click()

def selecionando_linha(driver):
    select = driver.find_element(By.CSS_SELECTOR, "#selectLinha")
    select_linha = Select(select)
    select_linha.select_by_value('MUN.CO_MUNICIPIO_IBGE')


def selecionando_coluna(driver):
    select = driver.find_element(By.CSS_SELECTOR, "#selectcoluna")
    select_linha = Select(select)
    select_linha.select_by_value('PCA')

    
def selecionando_tipo_producao(driver):
    select = driver.find_element(By.CSS_SELECTOR, "#tpProducao")
    select_linha = Select(select)
    select_linha.select_by_value('4')
 
def selecionando_problemacondicao(driver):
    labels = driver.find_elements(By.CSS_SELECTOR, "#filtrosAtendIndividual > div > div > div > label")
    for i, l in enumerate(labels):
        if l.text == "Problema/Condição Avaliada":
            pca_label = l
    parente = pca_label.find_element(By.XPATH,'..')
    botao = parente.find_element(By.TAG_NAME, "button")
    botao.click()
    seleciona_tudo = parente.find_element(By.CSS_SELECTOR, "input[value='multiselect-all']")
    seleciona_tudo.click()
    botao.click()


def selecionando_download(driver):
    download_button = driver.find_element(By.CSS_SELECTOR, "i.fa-download").find_element(By.XPATH, '..')
    download_button.click()
    csv_button = download_button.find_element(By.XPATH, "../ul/li[2]")
    csv_button.click()

def check_for_csv(path):
    resultado = list(path.glob("*.csv"))
    return len(resultado) > 0 

def move_arquivo_temporario(path, novo_path):
    old_path = list(path.glob("*.csv"))[0] 
    old_path.rename(novo_path)

def list_competencias_online(driver):
    select_competencias = driver.find_element(By.NAME, "j_idt76")
    select = Select(select_competencias)
    return [x.get_attribute("value") for x in select.options]

def list_competencias_baixadas(caminho):
    lista = [] 
    for x in caminho.glob("*.log"): 
        lista.append(x.stem)
    return lista


def main():
    # ../raw_data/temp
    caminho_download = Path(__file__).parent.parent / 'raw_data/temp'
    # ../raw_data/SISAB
    caminho_final =  caminho_download.parent / 'SISAB'

    # cria um driver que vai fazer download na pasta especificada
    driver = create_driver(caminho_download.as_posix()) 
    driver.get(URL)

    # espera a pagina carregar até aparecer o botão download
    criterio = (By.CLASS_NAME, "fa-download")
    wait = WebDriverWait(driver, timeout=15)
    wait.until(visibility_of_all_elements_located( criterio ))
 
    # ajustes que são indepententes da competência escolhida
    selecionando_linha(driver)
    selecionando_coluna(driver)
    selecionando_tipo_producao(driver)
    selecionando_problemacondicao(driver)

    # pegamos as competências disponíveis do próprio site
    competencias_disponiveis = list_competencias_online(driver)
    # pegamos o que já foi baixado 
    competencias_baixadas = list_competencias_baixadas(caminho_final)
    for x in competencias_baixadas:
        competencias_disponiveis.remove(x) # e removemos da lista do que baixar
    
    for x in competencias_disponiveis:
        selecionando_competencia(driver, x)
        selecionando_download(driver) 
        download_completo = False
        while not download_completo:
            sleep(0.2)
            download_completo = check_for_csv(caminho_download)
        move_arquivo_temporario(caminho_download, caminho_final / f"{x}.log")
        selecionando_competencia(driver, x)
    
    driver.quit() 


if __name__ == "__main__":
    main()