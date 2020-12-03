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
    
    for i in range(3): # loop the try-part (i.e. opening the link) until it works, but only try it 4 times at most#
        try: #try the following:#
          random_sleep_link = random.uniform(10, 15) #sleep for a random chosen amount of seconds between 10 and 15 seconds#
          time.sleep(random_sleep_link)
          open_page(driver, url) #access the URL using the header settings defined earlier#
      
        except requests.exceptions.RequestException: #if anything weird happens...#
          random_sleep_except = random.uniform(240,360)
          print("I've encountered an error! I'll pause for"+str(random_sleep_except/60) + " minutes and try again \n")
          time.sleep(random_sleep_except) #sleep the script for x seconds and....#
          continue #...start the loop again from the beginning#
      
        else: #if the try-part works...#
          break #...break out of the loop#

    else: #if x amount of retries on the try-part don't work...#
        raise Exception("Something really went wrong here... I'm sorry.") #...raise an exception and stop the script#

# if the script survived this part...# 
    
    page_counter = 1
    record_counter = 0
    num = 0
    
    link_list = get_links(driver)
    
    #Loop through the scraping code until we get 6000 records
    
    while page_counter < page_counter_limit:
            
            #Ensure main search results populate before further action is taken
        retries = 0
        while retries <= 5:
            
            try:
                
                main = WebDriverWait(driver,5).until(
                    EC.presence_of_element_located((By.ID, 'content')))
            except TimeoutException:
                    driver.refresh()
                    retries += 1
            
            link_list = get_links(driver)
            
            #Loop over links and get pertinent information
            
            for link in link_list:
                
                try:
                    appenders = scrape_link_details(driver,link)
                    
                    mylists = [num_sales, num_basket, descriptions, days_to_arrival, cost_delivery, returns_accepted, dispatch_from, count_images]
                    
                    for x, lst in zip(appenders, mylists):
                        lst.append(x)
                
                except:
                    break
                
                driver.back()
            
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


    
driver.quit()

data = {'Title': titles, 'Shop_Name':shop_names,'Is_Ad': is_ad, 'Star_Rating': star_ratings, 'Num_Reviews': num_reviews, 'Price': prices, 'Is_Bestseller': bestseller, 'Num_Sales': num_sales, 'Num_Basket': num_basket, 'Description': descriptions, 'Days_to_Arrival': days_to_arrival, 'Cost_Delivery': cost_delivery, 'Returns_Accepted': returns_accepted, 'Dispatched_From': dispatch_from, 'Num_Images': count_images, 'Category': category}

#Create dataframe from our dictionary  
            
df = pd.DataFrame(data)
df['Shop_Name'] = df['Shop_Name'].astype('category').cat.codes

#Save dataframe to a new CSV 

df.to_csv('raw_data.csv')