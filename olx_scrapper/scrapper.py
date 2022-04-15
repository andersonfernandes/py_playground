from dw import insert_place, insert_mobile, insert_advertiser, insert_date, insert_fact_ads, insert_TPM_ETL, close_db_connection
from chrome_driver import get_driver, find_element_by_xpath, wait_element_load

driver = get_driver()
driver.get('https://al.olx.com.br/celulares')
wait_element_load('ad-list')

# TODO: pagination
for i in range(10):
    try:
        link_base_xpath = '//*[@id="ad-list"]/li[' + str(i + 1) + ']'
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
        brand = find_element_by_xpath(content_base_xpath + 'div[22]/div/div/div/div[2]/div[2]/div/a').text
        condition = find_element_by_xpath(content_base_xpath + 'div[22]/div/div/div/div[2]/div[3]/div/a').text
        publication_data = find_element_by_xpath(content_base_xpath + 'div[26]/div/div/div/span[1]').text

        wait_element_load('miniprofile')
        advertiser_name = find_element_by_xpath('//*[@id="miniprofile"]/div/div/div/div[2]/div/span').text

        list_str_date = publication_data.split()
        list_month_day = list_str_date[2].split('/')

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
        if ',' in where:
            city, district = where.split(' - ')[0].split(', ')
        else:
            city, _ = where.split(' - ')
            district = 'unknown'

        real, amount = price.split(' ')

        insert_TPM_ETL(brand, title, condition, float(amount), advertiser_name, hour=list_str_date[4], day=list_month_day[0], moth=list_month_day[1], city=city,  district=district)
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
