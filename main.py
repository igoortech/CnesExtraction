from selenium import webdriver
from Libs import common_selenium
from Libs import common_funcoes
from selenium.webdriver.common.by import By
import time
import os
import pandas as pd
import csv
from selenium.webdriver.chrome.options import Options


# Definindo as variaveris
url = 'https://cnes.datasus.gov.br/pages/estabelecimentos/consulta.jsp'
url_ficha = 'https://cnes.datasus.gov.br/pages/estabelecimentos/ficha/index.jsp?coUnidade='

# Define a pasta de download
diretorio_atual = os.getcwd()
download_pasta = fr'{diretorio_atual}\Output'

input_f = fr'{diretorio_atual}\Input'
input_file = fr'{input_f}\InputFile.csv'

arquivo = fr'{download_pasta}\fichaCompletaEstabelecimento.pdf'
caminho_output = fr'{download_pasta}\cnes_files'
dados_completos = []

# Verifica se pasta  download existe
if not os.path.exists(download_pasta):
    os.makedirs(download_pasta)


# Verifica se a pasta input existe
if not os.path.exists(caminho_output):
    os.makedirs(caminho_output)


############## CONFIGURAÇÕES CHROME DRIVER#####################################
options = Options()
options.add_experimental_option('prefs', {
    'download.default_directory': download_pasta,
    'download.prompt_for_download': False,
    'download.directory_upgrade': True,
    'safebrowsing.enabled': True})

driver = webdriver.Chrome(options=options)
driver.implicitly_wait(30)
#########################################################################




# Realiza 3 tentativas
for i in range(0, 3):
   
    try:
    # LER O CONFIG FILE E OBTEM ESTADOS, MINICIPIOS
        with open(input_file, 'r', encoding="utf-8") as file:
            reader = csv.reader(file)
            next(reader)  # Ignora o cabeçalho
        
            # Percorre os estados
            for row in reader:
                estado = row[0].upper()  # estado
                municipio = row[1].upper()  # municipio
              
                # Valida se já obteve os dados antes
                caminho_arquivo = fr'{caminho_output}\{estado}_cnes_.xlsx'

                if not os.path.exists(caminho_arquivo):
                    print("Arquivo não existe!")
                    
                    # Navegar até a página que contém a tabela
                    driver.get(url)

                    
                    common_selenium.aguardar_elemento_ser_clicavel_xpath(driver, '//*[@id="logo"]/a/img', 20)

                    # PESQUISA UF
                    common_selenium.seleciona_uf(driver, '/html/body/div[2]/main/div/div[2]/div/form[1]/div[2]/div[1]/div/select', estado)
                    common_selenium.seleciona_uf(driver, '/html/body/div[2]/main/div/div[2]/div/form[1]/div[2]/div[2]/div/select', municipio)
                    common_selenium.clicar(driver, '/html/body/div[2]/main/div/div[2]/div/form[2]/div/button')
                    common_selenium.aguardar_elemento_ser_clicavel_xpath(driver, '/html/body/div[2]/main/div/div[2]/div/div[3]/table/thead/tr[1]/th[1]/div/span', 30)

                    # Percorrer as 5 páginas obtendo valores dinamicos
                    code = False
                    for index in range(0, 5):
                        

                        # contador para validação de linhas inválidas
                        contador = 0
                        # Localizar a tabela
                        uf = common_selenium.obter_tabela(driver, '/html/body/div[2]/main/div/div[2]/div/div[3]/table')

                        # Obter todas as linhas da tabela
                        linhas = uf.find_elements(By.TAG_NAME, "tr")

                        # Percorrer cada linha
                        for linha in linhas:
                            dados_completos = []
                            # elimina as primeiras linhas inválidas
                            if contador == 0 or contador == 1:
                                contador = contador + 1
                                continue

                            # Obtém o código de municipio para montar URL DE FICHA
                            if contador == 2 and code == False:
                                common_selenium.clicar(driver, '/html/body/div[2]/main/div/div[2]/div/div[3]/table/tbody/tr[1]/td[8]/button')
                                common_selenium.aguardar_elemento_ser_clicavel_xpath(driver, '//*[@id="dadosBasicosModal"]/div/div/div[3]/button', 20)
                                time.sleep(1)
                                municipio_code = common_selenium.obter_valores(driver, '/html/body/div[2]/main/div/div[2]/div/div[4]/div/div/div[2]/div/form/div[4]/div[2]/div/input')[:6]
                                common_selenium.clicar(driver, '//*[@id="dadosBasicosModal"]/div/div/div[3]/button')
                                code = True
                    
                            # obtém as colunas da linha
                            colunas = linha.find_elements(By.TAG_NAME, "td")
                            time.sleep(1)

                            # Extrair valor das colunas
                            if len(colunas) != 0:
                                uf = colunas[0].text
                                municipio = colunas[1].text
                                CNES = colunas[2].text
                                Nome_Fantasia = colunas[3].text
                                Natureza = colunas[4].text
                                Gestao = colunas[5].text
                                Atende_SUS = colunas[6].text
                                # adicicionando valores e url de qual ficha acessar posteriormente a lista
                                dados_completos.append([uf,municipio,CNES,Nome_Fantasia,Natureza,Gestao,Atende_SUS,url_ficha+municipio_code+CNES,'A processar'])

                                #gera o excel com dados do estado e coluna de controle
                                common_funcoes.gerar_excel_output(dados_completos,caminho_arquivo)

                            contador = contador + 1
                        # vai para próxima tabela
                        common_selenium.clicar(driver, '//*[@ng-switch-when="next"]')
                        common_selenium.aguardar_elemento_ser_clicavel_xpath(driver, '/html/body/div[2]/main/div/div[2]/div/div[3]/table/thead/tr[1]/th[1]/div/span', 30)
    
                        #Atualiza status de download para caso dê erro.
                        
                        # Iniciando download de fichas

            
                #Inicializa configurações da sheet de controle
                linha_atual = 1
                excel_sheet_index = 0
                common_funcoes.set_cell_sheet_index(caminho_arquivo,excel_sheet_index,'I1','STATUS')
                df = pd.read_excel(caminho_arquivo)
            
                for index, ficha in  df.iterrows():
                    linha_atual = linha_atual +  1
                    CNES = ficha['Cnes']
                    url_ficha = ficha['url_ficha']
                    status = ficha['STATUS']

                    if status != 'A processar':
                        continue
                    # percorrendo cada página para obter ficha
                    driver.get(url_ficha)

                    # Clicando botão imprimir ficha completa
                    common_selenium.clicar(driver, "//*[@class='glyphicon glyphicon-print']")

                    # Clicando para selecionar ficha completa
                    common_selenium.aguardar_elemento_ser_clicavel_xpath(driver, "//*[@id='todos']", 30)
                    common_selenium.clicar(driver, "//*[@id='todos']")

                    # clicando imrprimir (dowmload do pdf)
                    common_selenium.clicar(driver, "(//*[@type='button'])[3]")

                    # aguardando e renomeaidno a ficha
                    novo_arquivo = f'{caminho_output}\{CNES}.pdf'
                    common_funcoes.aguardar_renomeia_move(arquivo, novo_arquivo)

                    common_funcoes.set_cell_sheet_index(caminho_arquivo,excel_sheet_index,f'I{linha_atual}','Sucesso')
                    # gerando arquivo excel de output


    except Exception as error:
         print(error)
         continue
    print("Todas extrações foram realizadas com sucesso!")
    break

    
