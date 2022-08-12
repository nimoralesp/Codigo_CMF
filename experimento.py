import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options

import pandas as pd
import time
from datetime import date
import calendar



from selenium import webdriver
from selenium.webdriver.chrome.service import Service



options = webdriver.ChromeOptions() 
options.add_argument('--headless')
options.add_argument('--window-size=1920,1080')


meses = ['Marzo', 'Junio', 'Septiembre', 'Diciembre']
mes_a_num = {'Marzo':3, 'Junio':6, 'Septiembre':9, 'Diciembre':12}
anos = [str(x) for x in range(2015, 2023)]

hoy = date.today()

for i in anos:
    for j in meses:
        
        if (  (hoy.strftime('%Y') == i) and (int(hoy.strftime('%m')) <= mes_a_num[j])  ):
            break


        s=Service('chromedriver.exe')#Service('D:\DOWNLOADS\chromedriver_win32\chromedriver.exe')
        driver = webdriver.Chrome(service=s)
        url='https://www.cmfchile.cl/institucional/estadisticas/merc_valores/intermediarioscbp_fecu_ifrs/intermediarioscbp_ifrs_index.php?lang=es'
        driver.get(url)

        # Mes
        mes = Select(driver.find_element('name','mes1'))
        mes.select_by_visible_text(j)

        # Ano
        ano = Select(driver.find_element('name','anno1'))
        ano.select_by_visible_text(i)

        # Consultar
        consultar = driver.find_element('xpath', '/html/body/div[2]/div[2]/div/div/div/div[4]/div/div[1]/form[1]/div/table/tbody/tr[4]/td[2]/input')
        driver.execute_script("arguments[0].click();", consultar)

        #time.sleep(2)

        tabla = driver.find_element('css selector', '#table > div > div > table')
        tabla = tabla.get_attribute('outerHTML')
        tabla = pd.read_html(tabla, decimal=',', thousands='.')[0]
        tabla['Fecha'] = j + ' de ' + i

        tabla.to_csv('experimento/' + j + '.' + i + '.csv', index=None)

        #time.sleep(2)
        driver.close()

# Cosas por arreglar que solamente busque hasta el mes que exista dato y no se caiga el script
# Listo!
