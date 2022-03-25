from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import csv
import os
import time

OUTPUT_FOLDER = './outputs/'
OUTPUT_FILE_PATH = OUTPUT_FOLDER + 'products.csv'

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

driver.get('https://al.olx.com.br/eletronicos-e-celulares')
wait.until(EC.presence_of_element_located((By.ID, 'ad-list')))

if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

if (os.path.exists(OUTPUT_FILE_PATH)):
    os.remove(OUTPUT_FILE_PATH)

# TODO: pagination
with open(OUTPUT_FILE_PATH, 'w') as file:
    writer = csv.writer(file)
    for i in range(55):
        try:
            product_link_xpath = '//*[@id="ad-list"]/li[' + str(i + 1) + ']/a'
            product_link_element = driver.find_element(By.XPATH, product_link_xpath)
            product_url = product_link_element.get_attribute('href')

            driver.execute_script('window.open("' + product_url + '");')
            driver.switch_to.window(driver.window_handles[-1])

            time.sleep(1)
            # TODO: Process product details

            driver.close()

            driver.switch_to.window(driver.window_handles[0])
            product_text_xpath = 'div/div[2]'
            product_text_element = product_link_element.find_element(By.XPATH, product_text_xpath)
            row_text = product_text_element.text.replace('\n', ',').split(',')

            # TODO: Save to the database
            writer.writerow(row_text)
        except Exception as e:
            print('Unable to find element with index: ' + str(i + 1))

print('\nGenerated file ' + OUTPUT_FILE_PATH)

driver.quit()
