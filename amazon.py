# -*- coding: utf-8 -*-
"""
Created on Sun Aug 25 17:12:52 2019

@author: muhammad.ahmed3
"""
from selenium import webdriver
import time
from selenium.common.exceptions import WebDriverException, NoSuchElementException
from selenium.common.exceptions import InvalidSelectorException, StaleElementReferenceException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common import keys
import pandas as pd
import os

# import mysql.connector

# def myconnection():
#    connection = mysql.connector.connect(
#    host="localhost:3306",
#    user="test",
#    passwd="=test123",
#    database="db_name"
#    )
#    return connection


scriptpath = os.path.realpath(__file__)
scriptpath = scriptpath.replace('amazon.py', 'chromedriver.dms')

driver = webdriver.Chrome(executable_path=scriptpath)
# driver = webdriver.Chrome()


driver.get('https://www.amazon.com/gp/movers-and-shakers')
time.sleep(2)

try:
    driver.find_element_by_css_selector('#zg_browseRoot > ul > li:nth-child(24) > a').click()
    print('Home And Kitchen Clicked')
    time.sleep(2)
except:
    print('excep')
    pass

count = 1
vendor_links = []

while True:
    print('On page ' + str(count) + ' of Home And Kitchen')
    main_page = driver.current_url
    count = count + 1
    pg_links = []
    all_links = driver.find_elements_by_class_name('zg-item')
    for i in all_links:
        pg_links.append(i.find_element_by_tag_name('a').get_attribute('href'))

    s_count = 1

    for i in range(len(pg_links) - 1, -1, -1):
        print('On link: ' + str(s_count))
        print('Link: ' + pg_links[i])
        driver.get(pg_links[i])
        time.sleep(2)

        skip = 0
        try:
            print('Trying to find other sellers on amazon located on below left corner')
            action = ActionChains(driver)
            action.move_to_element(
                driver.find_element_by_id('mbc').find_elements_by_class_name('mbcMerchantName')[0]).perform()
            time.sleep(3)
            sel_link = driver.find_element_by_class_name('mbcPopoverContainer').find_element_by_tag_name(
                'a').get_attribute('href')
            time.sleep(1)
            print('Vendor name: ' + driver.find_element_by_id('mbc').find_elements_by_class_name('mbcMerchantName')[
                0].text)
            print('Vendor amazon link: ' + sel_link)
            vendor_links.append(sel_link)
            continue
        except BaseException as e:
            print(e)
            print('didnt find find other sellers on amazon located on below left corner')
            pass

        print('Trying to find See All Buying Options in this page.....')
        try:
            a_tags = driver.find_elements_by_tag_name('a')
            for i in a_tags:
                if 'See All Buying Options' in i.text:
                    print('See All Buying Options founded..........Clicking...')
                    i.click()
                    print('Clicked')
                    time.sleep(3)
                    try:
                        print('Finding vendors......')

                        try:
                            vendors = driver.find_elements_by_class_name('olpSellerColumn')
                            print('Total vendors found are: ' + str(len(vendors)))
                            for i in vendors:
                                if i.text != '':
                                    print('Vendor: ' + i.text)
                                    print(
                                        'Vendor amazon link: ' + i.find_element_by_tag_name('a').get_attribute('href'))
                                    vendor_links.append(i.find_element_by_tag_name('a').get_attribute('href'))
                                    break
                        except:
                            pass

                        vendors = driver.find_elements_by_id('aod-offer-soldBy')
                        print('Total vendors found are: ' + str(len(vendors)))
                        if len(vendors) == 0:
                            print('No vendors found for he above link')
                            break
                        for i in vendors:
                            print('Vendor: ' + i.text)
                            print('Vendor amazon link: ' + i.find_element_by_tag_name('a').get_attribute('href'))
                            vendor_links.append(i.find_element_by_tag_name('a').get_attribute('href'))
                            break
                    except:
                        print('No vendors found for he above link')
                        break
                        pass
        except:
            print('No vendors found for he above link')
            break
            pass

        if s_count == 10:
            break
        s_count = s_count + 1

    try:
        driver.get(main_page)
        time.sleep(2)
        print('Trying to go to next page............ i.e page no: ' + str(count))
        check_url = driver.current_url
        driver.find_element_by_class_name('a-last').click()
        if check_url == driver.current_url:
            print('No next page found. Total pages were: ' + str(count))
            break
    except:
        print('No next page found. Total pages were: ' + str(count))
        break
        pass

print('All vendors located.......')
print('Targeting all vendors to get their products.........')
print('Total vendors located are: ' + str(len(vendor_links)))

for i in vendor_links:
    driver.get(i)
    time.sleep(2)
    print('On Vendor link ' + i)
    v_name = driver.find_element_by_id('sellerName').text
    print('Vendor name: ' + v_name)
    driver.get(driver.find_element_by_id('storefront-link').find_element_by_tag_name('a').get_attribute('href'))
    time.sleep(2)
    print('On vendors page....')
    v_page = 1

    plink = []
    price = []
    vname = []

    while True:
        print('On vendors page: ' + str(v_page))
        v_page = v_page + 1

        links_all = driver.find_elements_by_class_name('a-spacing-medium')

        for i in links_all:
            try:
                p = float(
                    i.find_element_by_class_name('a-price').text.replace(' ', '').replace('$', '').replace('\n', '.'))
                #                print(p)
                #                print(i.find_element_by_class_name('a-link-normal').get_attribute('href'))
                #                print(i.find_element_by_class_name('a-size-base').text.replace(',',''))
                r = i.find_element_by_class_name('a-size-base').text.replace(',', '')
                if p >= 15 and p <= 30 and r <= 75:
                    price.append(p)
                    plink.append(i.find_element_by_class_name('a-link-normal').get_attribute('href'))
                    vname.append(v_name)
            except:
                pass

            try:
                print(i.find_elements_by_tag_name('span')[1].text)
                if '$' in i.find_element_by_tag_name('span').text:
                    p = i.find_element_by_tag_name('span').text.replace('$', '').replace(' ', '')
                    p = float(p)
                    #                    print(p)
                    if p >= 15 and p <= 30:
                        price.append(i.find_element_by_tag_name('span').text)
                        plink.append(i.get_attribute('href'))
                        vname.append(v_name)
            except:
                pass

        try:
            print('Trying to go to next page............ i.e page no: ' + str(v_page))
            driver.find_element_by_class_name('a-last').click()
        except:
            print('No next page found. Total pages were: ' + str(v_page))
            break
            pass

    df = pd.DataFrame(columns=["Vendor", "Product Link", "Price"],
                      data={"Vendor": vname, "Product Link": plink, "Price": price})
    df.to_csv("./ " + v_name + "_Products.csv", sep=',', index=False)
    print('Csv file for ' + v_name + ' successfully generated')

#    connection = myconnection()
#    for j in range(0,len(vname)):
#        sql_querry = 'insert into table_namer (Vendor,ProductLink,Price) values (%s,%s,%s)'
#        insert_tuple = (str(vname[j]), str(plink), str(price[j]))
#        cursor = connection.cursor(buffered=True)
#        cursor.execute(sql_querry,insert_tuple)
#        connection.commit()
#    cursor.close()
#    connection.close()


print('finished...............')
driver.quit()


