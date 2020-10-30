# -*- coding: utf-8 -*-
"""
Created on Sun Oct 25 16:24:40 2020
@author: Anastasia
"""

from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time

import pandas as pd 

from scraper_functions import open_page

#Establish path to Chromedriver

PATH = "C:/Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)

#Establish connection to URL

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
# free_uk = []
# bestseller = []
# discounted = []

local_seller = []
num_sales = []
in_basket = []
descriptions = []
est_arrival = []
cost_delivery = []
returns_accepted = []
dispatch_from = []
count_images = []

#Loop through the scraping code until we get 6000 records

# while record_counter < 10:
    
    #Ensure main search results populate before further action is taken

try:
    main = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'content')))
    
    #Get the listing containers and loop through them
    
    results = main.find_elements_by_xpath('//li[starts-with(@class, "wt-list-unstyled wt-grid__item-xs-6 wt-grid__item-md-4 wt-grid__item")]')[:65]
    
    print(len(results))
            
    for result in results: 
        
        title = result.find_element_by_css_selector("div > a[href]").get_attribute("title")
        titles.append(title)
    
        shop_name = result.find_element_by_css_selector("p.screen-reader-only").text
        if shop_name[:2] == 'Ad':
            is_ad.append(1)
        else:
            is_ad.append(0)
        shop_names.append(shop_name.split(" ")[-1])
        
        star_rating = result.find_element_by_css_selector("span.screen-reader-only").text
        star_ratings.append(star_rating.split(" ")[0])
        
        num_review = result.find_element_by_css_selector('span.text-body-smaller.text-gray-lighter.display-inline-block.icon-b-1').text
        num_reviews.append(num_review.strip("()"))
        
        price = result.find_element_by_css_selector('span.currency-value').text
        prices.append(price)
        
        #Initialize an empty list to hold links to each job search result 
        
        link_list = []
        
        #Find links for each job posted and append them to our links list 
        
        links = driver.find_elements_by_xpath("//div[starts-with(@class, 'js-merch-stash-check-listing')]/a[1]")
        
        for link in links:
            link_text = link.get_attribute("href")
            link_list.append(link_text)
        
        #Loop over links and get pertinent information
        
        for link in link_list:
            driver.get(link)
            
            try:
                loaded = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "gnav-search")))

            
                local = loaded.find_elements_by_css_selector('span.wt-text-caption.wt-nudge-r-2')
                if not local: local_seller.append(0)
                else: local_seller.append(1)
                
                sales = loaded.find_elements_by_xpath("//a[@class='wt-text-link-no-underline wt-display-inline-flex-xs wt-align-items-center']/span[2]")
                for x in sales:
                    conv_x = x.text
                    num_sales.append(conv_x.split(" ")[0])
                
                driver.back()
                wait = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'content')))
            except:
                break
        
        print(num_sales)
        
finally: 
                
    driver.quit()