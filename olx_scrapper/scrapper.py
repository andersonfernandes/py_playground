import time
from dw import insert_place, insert_mobile, insert_advertiser, insert_date, close_db_connection
from chrome_driver import get_driver, find_element_by_xpath, wait_element_load

driver = get_driver()
driver.get('https://al.olx.com.br/celulares')
wait_element_load('ad-list')

# TODO: pagination
for i in range(6):
    try:
        product_link_xpath = '//*[@id="ad-list"]/li[' + str(i + 1) + ']/a'
        product_link_element = find_element_by_xpath(xpath=product_link_xpath)
        product_url = product_link_element.get_attribute('href')
    
        # Open ad on a new window
        #driver.find_element_by_xpath('//*[@id="ad-list"]/li[' + str(i + 1) + ']/a/div/div[2]/div[1]/div[1]/div[1]/h2').click()       
        driver.execute_script('window.open("' + product_url + '");')
        driver.switch_to.window(driver.window_handles[-1])
        time.sleep(3)
        
        brand = driver.find_element_by_xpath('//*[@id="content"]/div[2]/div/div[2]/div[1]/div[22]/div/div/div/div[2]/div[2]/div/a').get_attribute('text')        
        state = driver.find_element_by_xpath('//*[@id="content"]/div[2]/div/div[2]/div[1]/div[22]/div/div/div/div[2]/div[3]/div/a').get_attribute('text')
        advertiserName = driver.find_element_by_xpath('//*[@id="miniprofile"]/div/div/div/div[2]/div/span').text
        publicationData = driver.find_element_by_xpath('//*[@id="content"]/div[2]/div/div[2]/div[1]/div[26]/div/div/div/span[1]').text
        listStrDate = publicationData.split()
        listMothDay = listStrDate[2].split('/')
      
        driver.close()        
        driver.switch_to.window(driver.window_handles[0]) # Go back to the main window

        product_text_xpath = 'div/div[2]'
        product_text_element = find_element_by_xpath(
            xpath=product_text_xpath,
            base_element=product_link_element
        )

        row_arr = product_text_element.text.replace('\n', '|').split('|')
        print(row_arr)

        if 'Online' in row_arr:
            row_arr.remove('Online')

        row_arr = [el for el in row_arr if 'de R$' not in el]

        # TODO: Fix this unpack
        title, price, *_, when, at, where, = row_arr
    
        city, district = where.split(' - ')[0].split(', ') 

        insert_place(city=city, district=district)
        insert_mobile(brand, title, state)
        insert_advertiser(advertiserName)
        insert_date(hour=listStrDate[4], day=listMothDay[0], moth=listMothDay[1])
        
    except Exception as e:
        print(e)
        # pass

close_db_connection()
driver.quit()
