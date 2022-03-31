from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

service = Service(ChromeDriverManager().install())
capabilities = DesiredCapabilities.CHROME
capabilities['pageLoadStrategy'] = 'none'
options = webdriver.ChromeOptions()
options.add_argument('--window-size=1920,1080')
options.add_argument('--disable-extensions')
options.add_argument("--proxy-server='direct://'")
options.add_argument('--proxy-bypass-list=*')
options.add_argument('--start-maximized')
options.add_argument('--disable-gpu')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--no-sandbox')
options.add_argument('--ignore-certificate-errors')
# options.add_argument('--headless')

driver = webdriver.Chrome(service=service, desired_capabilities=capabilities, options=options)
wait = WebDriverWait(driver, 20)

def get_driver():
    return driver

def find_element_by_xpath(xpath, base_element=driver):
    return base_element.find_element(By.XPATH, xpath)

def wait_element_load(element_id):
    wait.until(EC.presence_of_element_located((By.ID, element_id)))
