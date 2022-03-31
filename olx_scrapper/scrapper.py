import time
from dw import insert_place, close_db_connection
from chrome_driver import get_driver, find_element_by_xpath, wait_element_load

driver = get_driver()
driver.get('https://al.olx.com.br/celulares')
wait_element_load('ad-list')

# TODO: pagination
for i in range(55):
    try:
        product_link_xpath = '//*[@id="ad-list"]/li[' + str(i + 1) + ']/a'
        product_link_element = find_element_by_xpath(xpath=product_link_xpath)
        product_url = product_link_element.get_attribute('href')

        # Open ad on a new window
        # driver.execute_script('window.open("' + product_url + '");')
        # driver.switch_to.window(driver.window_handles[-1])
        #
        # time.sleep(1)
        # driver.close()
        # driver.switch_to.window(driver.window_handles[0]) # Go back to the main window

        product_text_xpath = 'div/div[2]'
        product_text_element = find_element_by_xpath(
            xpath=product_text_xpath,
            base_element=product_link_element
        )

        row_arr = product_text_element.text.replace('\n', '|').split('|')

        if 'Online' in row_arr:
            row_arr.remove('Online')

        row_arr = [el for el in row_arr if 'de R$' not in el]

        # TODO: Fix this unpack
        title, price, when, at, where, *_ = row_arr
        city, district = where.split(' - ')[0].split(', ')

        insert_place(city=city, district=district)
    except Exception as e:
        # print(e)
        pass

close_db_connection()
driver.quit()
