from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.webdriver import WebDriver
import time


def aguardar_elemento_ser_clicavel_xpath(driver: WebDriver, xpath: str, tempo: int)->bool:
    aguardar = WebDriverWait(driver, tempo)
    return aguardar.until(EC.element_to_be_clickable((By.XPATH, xpath)))

def seleciona_uf(driver: WebDriver,xpath: str,estado)-> None:
        elemento = driver.find_element(By.XPATH, xpath)
        time.sleep(1)
        drop=Select(elemento)
        time.sleep(1)
        drop.select_by_visible_text(estado)
        time.sleep(1)

def clicar(driver: WebDriver,xpath: str)->None:
      aguardar = WebDriverWait(driver, 30)
      elemento_encontrado = aguardar.until(EC.element_to_be_clickable((By.XPATH, xpath)))
      if elemento_encontrado:
            driver.find_element(By.XPATH,xpath).click()

def obter_tabela(driver: WebDriver,xpath: str):
      tabela_cnes = driver.find_element(By.XPATH,xpath)
      return tabela_cnes

def obter_valor(driver: WebDriver,xpath: str):
      valor = driver.find_element(By.XPATH,xpath)
      return valor.get_attribute('value')


def obter_valores(driver: WebDriver,xpath: str):
      valor = driver.find_element(By.XPATH,xpath)
      return valor.get_attribute('value')