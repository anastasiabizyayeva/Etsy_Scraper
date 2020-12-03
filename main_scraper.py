# -*- coding: utf-8 -*-
"""
Created on Sun Oct 25 16:24:40 2020
@author: Anastasia
"""

from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

import requests
import random
import time 

import pandas as pd 
import numpy as np

from scraper_functions import open_page, get_url_list, get_links, scrape_link_details, get_main_page, next_page
from scraper_options import PATH, search_terms, page_counter_limit

#Establish path to Chromedriver

driver = webdriver.Chrome(PATH)

#Establish connection to URLs

urls, terms = get_url_list(search_terms)

term_counter = 0

#Create empty lists to hold results 

titles = []
shop_names = []
is_ad = []
star_ratings = []
num_reviews = []
prices = []
bestseller = []
category = []

num_sales = []
num_basket = []
descriptions = []
days_to_arrival = []
cost_delivery = []
returns_accepted = []
dispatch_from = []
count_images = []

total_records = 0

# **WHEN EVERYTHING WORKS IMPLEMENT THIS CODE BELOW/ INDENT**
for url in urls:
    
    open_page(driver,url)
    
    page_counter = 1
    record_counter = 0
    num = 0
        
    #Loop through the scraping code until we get 6000 records
    
    while page_counter < page_counter_limit:
            
            #Ensure main search results populate before further action is taken
        retries = 0
        while retries <= 5:
            
            try:
                
                main = WebDriverWait(driver,10).until(
                    EC.presence_of_element_located((By.ID, 'content')))
            except TimeoutException:
                    driver.refresh()
                    retries += 1
            
            link_list = get_links(driver)
            print(len(link_list))
            #Loop over links and get pertinent information
            
            for link in link_list:
                
                try:
                    appenders = scrape_link_details(driver,link)
                    
                    mylists = [num_sales, num_basket, descriptions, days_to_arrival, cost_delivery, returns_accepted, dispatch_from, count_images]
                    
                    for x, lst in zip(appenders, mylists):
                        lst.append(x)
                        
                    print('success')
                
                except:
                    break
                
                # driver.back()
            
            # Get the listing containers and loop through them
            
            main = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.ID, 'content')))
            
            results = main.find_elements_by_xpath('//li[starts-with(@class, "wt-list-unstyled wt-grid__item-xs-6 wt-grid__item-md-4 wt-grid__item")]')[:65]
    
            record_counter += len(results)
                    
            for result in results:
                
                try:
                    info = get_main_page(driver, result, terms[term_counter])
                    info_list = [titles, is_ad, shop_names, star_ratings, num_reviews, prices, bestseller, category]
                    
                    for x, lst in zip(info, info_list):
                        lst.append(x)
                except: 
                    break
      
            print('Finished scraping page ' + str(page_counter) + ' of "' + terms[term_counter] + '" search term.')
            print('Scraped ' + str(record_counter) + ' records' + ' of "' + terms[term_counter] + '" search term.')
            print('Are all lists equal? ' + str(len(count_images) == record_counter))
            print()
                
            page_counter += 1
            
            try:
                next_page(driver, page_counter)
            except:
                print('no next page')
                break
            
            # print(len(count_images))
            # print(record_counter)
            # print(len(titles))
                
    total_records += record_counter
    
    print('Finished scraping search term. Total records for "' + terms[term_counter] + '": ' + str(record_counter))
    print('Total records in scrape: ' + str(total_records))
    print('Are all lists equal? ' + str(len(count_images) == total_records))
    print()
    
    term_counter += 1
    
            # print(len(titles))
            # print(len(shop_names))
            # print(len(is_ad))
            # print(len(star_ratings))
            # print(len(num_reviews))
            # print(len(prices))  
            # print(len(category))
    
            # print(len(num_sales))
            # print(len(num_basket))
            # print(len(descriptions))
            # print(len(days_to_arrival))
            # print(len(cost_delivery))
            # print(len(returns_accepted))
            # print(len(dispatch_from))
            # print(len(count_images))

            # print(titles[7:8])
            # print(descriptions[7:8])

    
driver.quit()

data = {'Title': titles, 'Shop_Name':shop_names,'Is_Ad': is_ad, 'Star_Rating': star_ratings, 'Num_Reviews': num_reviews, 'Price': prices, 'Is_Bestseller': bestseller, 'Num_Sales': num_sales, 'Num_Basket': num_basket, 'Description': descriptions, 'Days_to_Arrival': days_to_arrival, 'Cost_Delivery': cost_delivery, 'Returns_Accepted': returns_accepted, 'Dispatched_From': dispatch_from, 'Num_Images': count_images, 'Category': category}

#Create dataframe from our dictionary  
            
df = pd.DataFrame(data)
df['Shop_Name'] = df['Shop_Name'].astype('category').cat.codes

#Save dataframe to a new CSV 

df.to_csv('raw_data.csv')