# -*- coding: utf-8 -*-
"""
Created on Sun Oct 25 16:24:40 2020
@author: Anastasia
"""

from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import pandas as pd 
import numpy as np

from scraper_functions import open_page, get_url_list, get_links, scrape_link_details, get_main_page, next_page
from scraper_options import PATH, search_terms

#Establish path to Chromedriver

driver = webdriver.Chrome(PATH)

#Establish connection to URLs

urls = get_url_list(search_terms)

# **WHEN EVERYTHING WORKS IMPLEMENT THIS CODE BELOW/ INDENT**
# for url in urls:
#     open_page(driver, url)

URL = "https://www.etsy.com/uk/search?q=birthday%20card"

open_page(driver,URL)

#Check if the listing is an ad - have a column for this. Starts with 'Ad by' 

#From base page scrape title, shop name, star rating, how many stars, price, whether there's free UK delivery, whether bestseller, whether discounted 

#From click in, scrape 1- local seller, 2-num sales, 3-'other people want this', 4-description, 5- estimated arrival, 6- cost to deliver, 7-whether returns are accepted, 8-where it dispatches from, 9-count of images 

#Initialize counts for page flipping and counting total records 

page_counter = 0
record_counter = 0
num = 0

#Create empty lists to hold results 

titles = []
shop_names = []
is_ad = []
star_ratings = []
num_reviews = []
prices = []
bestseller = []

num_sales = []
num_basket = []
descriptions = []
est_arrival = []
cost_delivery = []
returns_accepted = []
dispatch_from = []
count_images = []

#Loop through the scraping code until we get 6000 records

while page_counter < 240:
        
        #Ensure main search results populate before further action is taken
    
    try:
        main = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'content')))
        
        link_list = get_links(driver)
        
        #Loop over links and get pertinent information
        
        for link in link_list:
            
            appenders = scrape_link_details(driver,link)
            
            mylists = [num_sales, num_basket, descriptions, est_arrival, cost_delivery, returns_accepted, dispatch_from, count_images]
            for x, lst in zip(appenders, mylists):
                lst.append(x)
            
            driver.back()
        
        #Get the listing containers and loop through them
        main = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'content')))
        
        results = main.find_elements_by_xpath('//li[starts-with(@class, "wt-list-unstyled wt-grid__item-xs-6 wt-grid__item-md-4 wt-grid__item")]')[:65]
        
        record_counter += len(results)
                
        for result in results: 
                
            info = get_main_page(driver, result)
            info_list = [titles, is_ad, shop_names, star_ratings, num_reviews, prices, bestseller]
            
            for x, lst in zip(info, info_list):
                lst.append(x)
  
        print('Finished scraping page ' + str(page_counter + 1))
        print('Scraped ' + str(record_counter) + ' records')
        print(len(count_images) == record_counter)
            
        page_counter += 1
        
        print(len(titles))
        print(len(shop_names))
        print(len(is_ad))
        print(len(star_ratings))
        print(len(num_reviews))
        print(len(prices))
        
        print(len(num_sales))
        print(len(num_basket))
        print(len(descriptions))
        print(len(est_arrival))
        print(len(cost_delivery))
        print(len(returns_accepted))
        print(len(dispatch_from))
        print(len(count_images))
        
        next_page(driver, page_counter)
        
        # page = driver.find_element_by_xpath('//a[contains(@href,"https://www.etsy.com/uk/search?q=birthday+card&ref=pagination&page={}")]'.format(1+page_counter))
        # next_page = page.get_attribute("href")
        # driver.get(next_page)
    
    except:
        break

driver.quit()

data = {'Title': titles, 'Shop_Name':shop_names,'Is_Ad': is_ad, 'Star_Rating': star_ratings, 'Num_Reviews': num_reviews, 'Price': prices, 'Is_Bestseller': bestseller, 'Num_Sales': num_sales, 'Num_Basket': num_basket, 'Description': descriptions, 'Est_Arrival': est_arrival, 'Cost_Delivery': cost_delivery, 'Returns_Accepted': returns_accepted, 'Dispatched_From': dispatch_from, 'Num_Images': count_images}

#Create dataframe from our dictionary  
            
df = pd.DataFrame(data)
df['Shop_Name'] = df['Shop_Name'].astype('category').cat.codes
df['Category'] = 'Valentine'

#Save dataframe to a new CSV 

df.to_csv('raw_data.csv')