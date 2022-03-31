from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import mysql.connector
import time
import re

service = Service(ChromeDriverManager().install())
capabilities = DesiredCapabilities.CHROME
capabilities['pageLoadStrategy'] = 'none'
options = webdriver.ChromeOptions()
options.add_argument('--window-size=1920,1080')
options.add_argument('--disable-extensions')
options.add_argument("--proxy-server='direct://'")
options.add_argument('--proxy-bypass-list=*')
options.add_argument('--start-maximized')
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--no-sandbox')
options.add_argument('--ignore-certificate-errors')

driver = webdriver.Chrome(service=service, desired_capabilities=capabilities, options=options)
wait = WebDriverWait(driver, 20)

driver.get('https://al.olx.com.br/celulares')
wait.until(EC.presence_of_element_located((By.ID, 'ad-list')))

database_connection = mysql.connector.connect(
    host='localhost',
    user='root',
    password='root',
    database='olx_database'
)

def insert_place(city, district, state='Alagoas'):
    cursor = database_connection.cursor()
    sql = "INSERT IGNORE INTO DM_LOCAL (CIDADE, BAIRRO, ESTADO) VALUES (%s, %s, %s)"
    cursor.execute(sql, (city, district, state))
    database_connection.commit()
    cursor.close()

# TODO: pagination
for i in range(55):
    try:
        product_link_xpath = '//*[@id="ad-list"]/li[' + str(i + 1) + ']/a'
        product_link_element = driver.find_element(By.XPATH, product_link_xpath)
        product_url = product_link_element.get_attribute('href')

        # driver.execute_script('window.open("' + product_url + '");')
        # driver.switch_to.window(driver.window_handles[-1])
        #
        # time.sleep(1)
        # driver.close()
        # driver.switch_to.window(driver.window_handles[0])

        product_text_xpath = 'div/div[2]'
        product_text_element = product_link_element.find_element(By.XPATH, product_text_xpath)
        row_arr = product_text_element.text.replace('\n', '|').split('|')

        if 'Online' in row_arr:
            row_arr.remove('Online')

        row_arr = [el for el in row_arr if 'de R$' not in el]

        # TODO: Fix this unpack
        title, price, when, at, where, *_ = row_arr
        city, district, *_ = where.replace(' -', ', ').split(', ')

        insert_place(city=city, district=district)
    except Exception as e:
        # print(e)
        pass

database_connection.close()
driver.quit()
