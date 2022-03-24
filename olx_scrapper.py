from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import pandas as pd
import csv
import os

OUTPUT_FILENAME = './outputs/products.csv'

service = Service(ChromeDriverManager().install())
capabilities = DesiredCapabilities.CHROME
capabilities["pageLoadStrategy"] = "none"
options = webdriver.ChromeOptions()
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument("--start-maximized")

driver = webdriver.Chrome(service=service, desired_capabilities=capabilities, options=options)
wait = WebDriverWait(driver, 20)

driver.get('https://al.olx.com.br/eletronicos-e-celulares')
wait.until(EC.presence_of_element_located((By.ID, 'ad-list')))

if (os.path.exists(OUTPUT_FILENAME)):
    os.remove(OUTPUT_FILENAME)

with open(OUTPUT_FILENAME, 'w') as file:
    writer = csv.writer(file)
    for i in range(55):
        try:
            product_text_xpath = '//*[@id="ad-list"]/li[' + str(i + 1) + ']/a/div/div[2]'
            product = driver.find_element(By.XPATH, product_text_xpath)
            row = product.text.replace('\n', ',').split(',')

            writer.writerow(row)
        except Exception as e:
            print('Unable to find element with index: ' + str(i + 1))

print('\nGenerated file ' + OUTPUT_FILENAME)

driver.quit()
