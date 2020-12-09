# -*- coding: utf-8 -*-
"""
Created on Sun Oct 25 16:24:40 2020
@author: Anastasia
"""

#Import statements 

from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time 

import pandas as pd 

#Import functions and options from other docs 

from scraper_functions import open_page, get_url_list, get_links, scrape_link_details, get_main_page, next_page
from scraper_options import PATH, search_terms, page_counter_limit

#Establish path to Chromedriver

driver = webdriver.Chrome(PATH)

#Establish connection to URLs and get list of terms to search

urls, terms = get_url_list(search_terms)

#Initialize term counter 

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

#Loop through search term URLs 

for url in urls:
    
    #Open the URL and close popup
    
    open_page(driver,url)
    
    #Initialize record and page counters 
    
    page_counter = 1
    record_counter = 0
        
    #Loop through pages in the URL until you reach your desired page limit - note that the Etsy limit is 240
    
    while page_counter < page_counter_limit:
            
        #Implement retry loop to prevent IP block stalling 
        
        retries = 0
        while retries <= 5:
            
            #Wait until page loads search contents before scraping 
            
            try:
                
                main = WebDriverWait(driver,10).until(
                    EC.presence_of_element_located((By.ID, 'content')))
                time.sleep(4)
            except:
                    driver.refresh()
                    retries += 1
            
            #Get a list of links to individual listings
            
            link_list = get_links(driver)
            
            #We only want to keep first 65 links because the rest are your 'recently viewed' links 
            
            link_list = link_list[:65]
            
            #Loop over links and get pertinent information
            
            for link in link_list:
                
                try:
                    appenders = scrape_link_details(driver,link)
                    
                    mylists = [num_sales, num_basket, descriptions, days_to_arrival, cost_delivery, returns_accepted, dispatch_from, count_images]
                    
                    for x, lst in zip(appenders, mylists):
                        lst.append(x)
                                        
                except:
                    break
                            
            # Get the listing containers and loop through them
            
            main = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.ID, 'content')))
            
            #Get only the first 65 listing containers - the rest are your 'recently viewed' items 
            
            results = main.find_elements_by_xpath('//li[starts-with(@class, "wt-list-unstyled wt-grid__item-xs-6 wt-grid__item-md-4 wt-grid__item")]')[:65]
            
            #Add the results you've scraped to your record counter 
            
            record_counter += len(results)
                    
            #Loop over each listing and get its details 
            
            for result in results:
                
                try:
                    info = get_main_page(driver, result, terms[term_counter])
                    info_list = [titles, is_ad, shop_names, star_ratings, num_reviews, prices, bestseller, category]
                    
                    for x, lst in zip(info, info_list):
                        lst.append(x)
                except: 
                    break
                
            #For each page, print out a statement telling you how many pages have been scraped, how many records have been scraped, and whether all scraped categories are equal. 
            
            print('Finished scraping page ' + str(page_counter) + ' of "' + terms[term_counter] + '" search term.')
            print('Scraped ' + str(record_counter) + ' records' + ' of "' + terms[term_counter] + '" search term.')
            print('Are all lists equal? ' + str(len(count_images) == record_counter))
            print()
            
            #Add one to the page count 
            
            page_counter += 1
            
            #Click into the next page 
            
            try:
                next_page(driver, page_counter)
            except:
                print('no next page')
                break

    #Get the total record count
    
    total_records += record_counter
    
    #Print the total number of records scraped for this term, as well as the total records overall. 
    
    print('Finished scraping search term. Total records for "' + terms[term_counter] + '": ' + str(record_counter))
    print('Total records in scrape: ' + str(total_records))
    print('Are all lists equal? ' + str(len(count_images) == total_records))
    print()
    
    #Add one to the term counter so the next term is scraped
    
    term_counter += 1

# Close driver 

driver.quit()

#Create a dict from our lists 

data = {'Title': titles, 'Shop_Name':shop_names,'Is_Ad': is_ad, 'Star_Rating': star_ratings, 'Num_Reviews': num_reviews, 'Price': prices, 'Is_Bestseller': bestseller, 'Num_Sales': num_sales, 'Num_Basket': num_basket, 'Description': descriptions, 'Days_to_Arrival': days_to_arrival, 'Cost_Delivery': cost_delivery, 'Returns_Accepted': returns_accepted, 'Dispatched_From': dispatch_from, 'Num_Images': count_images, 'Category': category}

#Create dataframe from our dictionary  
            
df = pd.DataFrame(data)

#Anonymize the shop names 

df['Shop_Name'] = df['Shop_Name'].astype('category').cat.codes

#Save dataframe to a new CSV 

df.to_csv('raw_data.csv')