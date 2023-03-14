from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import pandas as pd
import time

# Leitura dos dados da planilha
df = pd.read_csv('./Parâmetros.csv')

# Lista de resultados
results = []

# Configuração do navegador Selenium
driver = webdriver.Chrome()

# Cria uma lista de palavras-chave a partir da planilha
keywords = [kw.strip() for kw in df['palavras_chave'].str.cat(sep=',').split(',')]

# Remove valores nulos da lista de URLs
urls = df['urls'].dropna().tolist()

# Iteração pelas URLs
for url in urls:
    print(url)
    # Acessa a página
    driver.get(url)
    # Espera a página carregar
    time.sleep(5)
    # Obtém o código-fonte da página
    source = driver.page_source
    soup = BeautifulSoup(source, 'html.parser')
    # Iteração pelas palavras-chave
    for keyword in keywords:
        # Verifica se a palavra-chave está presente na página
        if keyword in soup.get_text():
            # Adiciona a URL e a palavra-chave aos resultados
            results.append({'URL': url, 'Palavra-chave': keyword})

# Fecha o navegador Selenium
driver.quit()

# Salva os resultados em uma nova planilha do Excel
result_df = pd.DataFrame(results)
result_df.to_excel('./Resultado.xlsx', index=False)
