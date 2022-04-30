from dw import insert_place, insert_mobile, insert_advertiser, insert_date, insert_fact_ads, insert_TPM_ETL, close_db_connection
from chrome_driver import get_driver, find_element_by_xpath, wait_element_load
from model_handling import apple_handling, samsung_handling, lg_handling, motorola_lenovo_handling

driver = get_driver()

state_list = ['al', 'se']

for initials in state_list:

    for page in range(80):
        driver.get(f'https://{initials}.olx.com.br/celulares?o={str(page + 1)}')
        wait_element_load('ad-list')

        for item in range(55):
            try:
            
                link_base_xpath = '//*[@id="ad-list"]/li[' + str(item + 1) + ']'
                product_link_xpath = f'{link_base_xpath}/div'
                product_link_element = find_element_by_xpath(xpath=product_link_xpath)

                product_link_element_class = product_link_element.get_attribute('class')
                pub_classes = ['yap-gemini-pub-item', 'listing-native-list-item-1-pub']
                if product_link_element_class in pub_classes:
                    continue

                product_link_element.click()
                driver.switch_to.window(driver.window_handles[-1])

                wait_element_load('content')

                content_base_xpath = '//*[@id="content"]/div[2]/div/div[2]/div[1]/'
                brand = find_element_by_xpath(content_base_xpath + 'div[22]/div/div/div/div[2]/div[2]/div/a').text.upper()
                condition = find_element_by_xpath(content_base_xpath + 'div[22]/div/div/div/div[2]/div[3]/div/a').text.upper()
                publication_data = find_element_by_xpath(content_base_xpath + 'div[27]/div/div/div/span[1]').text.upper()

                wait_element_load('miniprofile')
                advertiser_name = find_element_by_xpath('//*[@id="miniprofile"]/div/div/div/div[2]/div').text.upper()

                list_str_date = publication_data.split()
                hour = list_str_date[4]
                list_month_day = list_str_date[2].split('/')
                day = int(list_month_day[0])
                moth = int(list_month_day[1])

                driver.close()
                driver.switch_to.window(driver.window_handles[0])

                product_text_xpath = 'a/div/div[2]'
                product_text_element = find_element_by_xpath(
                    xpath=product_text_xpath,
                    base_element=product_link_element
                )
            
                row_arr = product_text_element.text.replace('\n', '|').split('|')

                for term in ['Online', 'ONLINE', 'de R$']:
                    row_arr = [el for el in row_arr if term not in el]
                
                print(row_arr)

                title, price, where, when = row_arr

                print(brand)
                if brand == 'APPLE':
                    model = apple_handling(title)
                elif brand == 'SAMSUNG':
                    model = samsung_handling(title)
                elif brand == 'LG':
                    model = lg_handling(title)
                elif brand == 'MOTOROLA E LENOVO':
                    model = motorola_lenovo_handling(title)  
                else:
                    continue      

                print(model)
                if model == None:
                    continue   

                if ',' in where:
                    city, district = where.split(' - ')[0].split(', ')
                else:
                    city, _ = where.split(' - ')
                    district = 'DESCONHECIDO'

                if initials == 'al':
                    state = 'ALAGOAS'
                elif initials == 'se':
                    state = 'SERGIPE'

                _, amount = price.split(' ')

                for i in amount:
                    amount = amount.replace('.','')

                insert_TPM_ETL(brand, model, condition, amount, advertiser_name, hour, day, moth, state, city=city.upper(), district=district.upper())
            
            except Exception as e:
                if len(driver.window_handles) > 1:
                    driver.close()
                    driver.switch_to.window(driver.window_handles[0])

                print(e)
                continue

insert_place()
insert_mobile()
insert_advertiser()
insert_date()
insert_fact_ads()

close_db_connection()
driver.quit()
