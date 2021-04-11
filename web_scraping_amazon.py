from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import csv
from bs4 import BeautifulSoup
from time import sleep
from datetime import datetime
from random import random


# Getting next page
def get_url(search_term):
    """Generate a url from search term"""
    template = 'https://www.amazon.com.br/s?k={}&__mk_pt_BR=%C3%85M%C3%85%C5%BD%C3%95%C3%91&ref=nb_sb_noss_1'
    search_term = search_term.replace(' ', '+')

    #add term query to url
    url =  template.format(search_term)

    #add page query placeholder
    url += '&page{}'

    return url


#Generalize the pattern
def extract_record(item):
    """Extract and return data from a single record"""
    # Description & url
    atag = item.h2.a
    description = atag.text.strip() # description
    url = 'https://www.amazon.com' + atag.get('href')

    try:
        #price
        price_parent = item.find('span','a-price') 
        price = price_parent.find('span','a-offscreen').text
    except AttributeError:
        return

    #rank and rating
    try:
        rating = item.i.text
        review_count = item.find('span',{'class':'a-size-base-plus a-color-base a-text-normal', 'dir':'auto'}).text
    except AttributeError:
        rating = ''
        review_count = ''
    
    result = (description, price, rating, review_count, url)

    return result


def main(search_term):
    #start webdriver
    path = "D:/VAL/PROJETOS_PYTHON/api_crawler_amazon/chrome-webDriver/chromedriver"
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    driver = webdriver.Chrome(executable_path=path, options=options)
   
    records = []
    url = get_url(search_term)
    

    for page in range(1, 21): # max of 20 pages
        driver.get(url.format(page))
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        #soup = BeautifulSoup(driver.page_source, 'lxml')
        results = soup.find_all('div', {'data-component-type':'s-search-result'})

        for item in results:
            record = extract_record(item)
            if record:
                records.append(record)

    driver.close()

    # save data into csv
    timestamp = datetime.now().strftime("%Y%m%d%H%S%M")
    with open('results'+ '_' + timestamp + '.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Description','Price','Rating','ReviewCount','Url'])
        writer.writerows(records)


main('ultrawide monitor')