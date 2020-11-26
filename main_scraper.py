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

from scraper_functions import open_page, get_url_list, get_links, scrape_link_details
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
            
            
            # driver.get(link)
        
            # loaded = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "gnav-search")))

            # try:
            #     sales = loaded.find_elements_by_xpath("//div[starts-with(@class, 'wt-display-inline-flex-xs wt-align-items-center')]/a/span[1]")
            #     s = sales[0].text
            #     num_sales = s.split(" ")[0]
            # except:
            #     num_sales = 0
                        
            # try:
            #     basket = loaded.find_elements_by_xpath("//p[@class='wt-position-relative wt-text-caption']")
            #     x = basket[0].text
            #     y = [int(i) for i in x.split() if i.isdigit()]
            #     num_basket = y
            # except:
            #     num_basket.append(0)
            
            # try:
            #     description = loaded.find_element_by_xpath("//meta[@name='description']")
            #     descriptions.append(description.get_attribute("content"))
            # except:
            #     descriptions.append(np.nan)
            
            # try:
            #     est = loaded.find_element_by_xpath("//*[contains(text(), 'Estimated arrival')]")
            #     arrival = loaded.find_element_by_xpath("//*[@id='shipping-variant-div']/div/div[2]/div[1]/div/div[1]/p")
            #     est_arrival.append(arrival.text)
            # except:
            #     est_arrival.append(np.nan)
            
            # try:
            #     delivery = loaded.find_element_by_xpath("//*[contains(text(), 'Cost to deliver')]/following-sibling::p").text
            #     cost_delivery.append(delivery)
            # except:
            #     cost_delivery.append(np.nan)
            
            # try:
            #     returns = loaded.find_element_by_xpath("//*[contains(text(), 'Accepted')]")
            #     returns_accepted.append(1)
            # except:
            #     returns_accepted.append(0)
            
            # try:
            #     dispatch = loaded.find_element_by_xpath("//*[@id='shipping-variant-div']/div/div[2]/div[7]").text
            #     d_split = dispatch.split(" ")[2:]
            #     d_join = " ".join(d_split)
            #     dispatch_from.append(d_join)
            # except:
            #     dispatch_from.append(np.nan)
            
            # try:
            #     images = loaded.find_element_by_xpath("//ul[starts-with(@class, 'wt-list-unstyled wt-display-flex-xs')]")
            #     i_list = images.find_elements_by_xpath("//li[@class='wt-mr-xs-1 wt-mb-xs-1 wt-bg-gray wt-flex-shrink-xs-0 wt-rounded carousel-pagination-item-v2']")
            #     count_images.append(len(i_list))
            # except:
            #     count_images.append(1)
            
            driver.back()
        
        #Get the listing containers and loop through them
        main = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'content')))
        
        results = main.find_elements_by_xpath('//li[starts-with(@class, "wt-list-unstyled wt-grid__item-xs-6 wt-grid__item-md-4 wt-grid__item")]')[:65]
        
        record_counter += len(results)
                
        for result in results: 
            
            title = result.find_element_by_css_selector("div > a[href]").get_attribute("title")
            titles.append(title)
        
            shop_name = result.find_element_by_css_selector("p.screen-reader-only").text
            if shop_name[:2] == 'Ad':
                is_ad.append(1)
            else:
                is_ad.append(0)
            shop_names.append(shop_name.split(" ")[-1])
            
            try:
                star_rating = result.find_element_by_css_selector("span.screen-reader-only").text
                star_ratings.append(star_rating.split(" ")[0])
            except:
                star_ratings.append(np.nan)
            
            try:
                num_review = result.find_element_by_css_selector('span.text-body-smaller.text-gray-lighter.display-inline-block.icon-b-1').text
                num_reviews.append(num_review.strip("()"))
            except:
                num_reviews.append(0)
            
            price = result.find_element_by_css_selector('span.currency-value').text
            prices.append(price)
                
            try:    
                b_seller = result.find_element_by_xpath("//span[@class='wt-badge wt-badge--small wt-badge--status-03']/span[2]")
                bestseller.append(1)
            except:
                bestseller.append(np.nan)  
                    
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
        
        page = driver.find_element_by_xpath('//a[contains(@href,"https://www.etsy.com/uk/search?q=birthday+card&ref=pagination&page={}")]'.format(1+page_counter))
        next_page = page.get_attribute("href")
        driver.get(next_page)
    
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