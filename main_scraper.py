# -*- coding: utf-8 -*-
"""
Created on Sun Oct 25 16:24:40 2020
@author: Anastasia
"""

from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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
unique_ids = []

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
    open_page(driver, url)
    
    page_counter = 1
    record_counter = 0
    num = 0
    
    link_list = get_links(driver, unique_ids)
    
    #Loop through the scraping code until we get 6000 records
    
    while page_counter < page_counter_limit:
            
            #Ensure main search results populate before further action is taken
        
        try:
            main = WebDriverWait(driver,5).until(
                EC.presence_of_element_located((By.ID, 'content')))
            
            link_list = get_links(driver, unique_ids)
            
            #Loop over links and get pertinent information
            
            for link in link_list:
                
                appenders = scrape_link_details(driver,link)
                
                mylists = [num_sales, num_basket, descriptions, days_to_arrival, cost_delivery, returns_accepted, dispatch_from, count_images]
                for x, lst in zip(appenders, mylists):
                    lst.append(x)
                
                driver.back()
            
            # Get the listing containers and loop through them
            main = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, 'content')))
            
            results = []
            
            options = main.find_elements_by_xpath('//li[starts-with(@class, "wt-list-unstyled wt-grid__item-xs-6 wt-grid__item-md-4 wt-grid__item")]')[:65]
            for i in options:
                check_id = i.find_element_by_xpath(".//div").get_attribute('data-listing-id')
                if check_id not in unique_ids:
                    unique_ids.append(i)
                results.append(i)
    
            record_counter += len(results)
                    
            for result in results:
                
                try:
                    
                    info = get_main_page(driver, result, terms[term_counter])
                    info_list = [titles, is_ad, shop_names, star_ratings, num_reviews, prices, bestseller, category]
                    
                    for x, lst in zip(info, info_list):
                        lst.append(x)
                except: 
                    break
      
            print('Finished scraping page ' + str(page_counter) + ' of "' + terms[term_counter] + '" records.')
            print('Scraped ' + str(record_counter) + ' records' + ' of "' + terms[term_counter] + '" records.')
            print('Are all lists equal? ' + str(len(count_images) == record_counter))
                
            page_counter += 1
            
            try:
                next_page(driver, page_counter)
            except:
                print('no next page')
                break
                        
        except:
            break
                
    total_records += record_counter
    
    print('Finished scraping search term. Total records for ' + terms[term_counter] + ': ' + str(record_counter))
    print('Total records in scrape: ' + str(total_records))
    
    term_counter += 1

    
driver.quit()

data = {'Title': titles, 'Shop_Name':shop_names,'Is_Ad': is_ad, 'Star_Rating': star_ratings, 'Num_Reviews': num_reviews, 'Price': prices, 'Is_Bestseller': bestseller, 'Num_Sales': num_sales, 'Num_Basket': num_basket, 'Description': descriptions, 'Days_to_Arrival': days_to_arrival, 'Cost_Delivery': cost_delivery, 'Returns_Accepted': returns_accepted, 'Dispatched_From': dispatch_from, 'Num_Images': count_images, 'Category': category}

#Create dataframe from our dictionary  
            
df = pd.DataFrame(data)
df['Shop_Name'] = df['Shop_Name'].astype('category').cat.codes

#Save dataframe to a new CSV 

df.to_csv('raw_data.csv')