# -*- coding: utf-8 -*-
"""
Created on Tue Oct 27 17:10:33 2020

@author: Anastasia
"""

#Import all packages

from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from daterangeparser import parse
import datetime
import requests
import random
import time 
import re 

import pandas as pd 
import numpy as np 

def get_url_list(search_list):
    url_list = []
    term_list=[]
    for term in search_list:
        url_list.append('https://www.etsy.com/uk/search?q=' + re.sub("\s", "+", term))
        term_list.append(term)
    return url_list, term_list
    
def close_popup(driver):
    pop_up_xpath = "//*[@id='gdpr-single-choice-overlay']/div/div[2]/div[2]/button"
    try:
        driver.find_element_by_xpath(pop_up_xpath).click()
        # time.sleep(2)
    except:
        pass
    
def open_page(driver, URL):
    for i in range(3): # loop the try-part (i.e. opening the link) until it works, but only try it 4 times at most#
        try: #try the following:#
          random_sleep_link = random.uniform(10, 15) #sleep for a random chosen amount of seconds between 10 and 15 seconds#
          time.sleep(random_sleep_link)
          driver.get(URL)
 #access the URL using the header settings defined earlier#
      
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
    close_popup(driver)

#Find links for each job posted and append them to our links list
def get_links(driver):
    
    #Initialize an empty list to hold links to each job search result 
    link_list = []
    links = driver.find_elements_by_xpath("//div[starts-with(@class, 'js-merch-stash-check-listing')]/a[1]")
    for link in links:
        link_text = link.get_attribute("href")
        link_list.append(link_text)
    return link_list

def scrape_link_details(driver,link):
    
    for i in range(3): # loop the try-part (i.e. opening the link) until it works, but only try it 4 times at most#
        try: #try the following:#
          random_sleep_link = random.uniform(1, 3)
          time.sleep(random_sleep_link)
          
          windows_before  = driver.current_window_handle # Store the parent_window_handle for future use
          
          # driver.get(link)  #access the URL using the header settings defined earlier#

          driver.execute_script("window.open('" + link +"');")
          windows_after = driver.window_handles
          new_window = [x for x in windows_after if x != windows_before][0] # Identify the newly opened window
          driver.switch_to.window(new_window) # switch_to the new window
          
          loaded = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "gnav-search")))
          try:
                sales = loaded.find_elements_by_xpath("//div[starts-with(@class, 'wt-display-inline-flex-xs wt-align-items-center')]/a/span[1]")
                s = sales[0].text
                num_sales = s.split(" ")[0]
          except:
                num_sales = 0
                        
          try:
                basket = loaded.find_elements_by_xpath("//p[@class='wt-position-relative wt-text-caption']")
                x = basket[0].text
                y = [int(i) for i in x.split() if i.isdigit()]
                for i in y:
                    num_basket = i
          except:
                num_basket = 0
            
          try:
                description = loaded.find_element_by_xpath("//meta[@name='description']")
                descriptions = description.get_attribute("content")
          except:
                descriptions = np.nan
            
          try:
                arrival = loaded.find_element_by_xpath("//*[@id='shipping-variant-div']/div/div[2]/div[1]/div/div[1]/p")
                arrival_range = arrival.text
                start, end = parse(arrival_range)
                average = start + (end - start)/2
                today = datetime.date.today()
                diff = average.date() - today
                days_to_arrival = diff.days
          except:
                days_to_arrival = np.nan
            
          try:
                delivery = loaded.find_element_by_xpath("//*[contains(text(), 'Cost to deliver')]/following-sibling::p").text
                if delivery == 'Free':
                    cost_delivery = 0
                else:
                    match = re.search(r'\d{1,3}(?:[.,]\d{3})*(?:[.,]\d{2})', delivery).group(0)
                    cost_delivery = float(match)
          except:
                cost_delivery = np.nan
            
          try:
                loaded.find_element_by_xpath("//*[contains(text(), 'Accepted')]")
                returns_accepted = 1
          except:
                returns_accepted = 0
            
          try:
                dispatch = loaded.find_element_by_xpath("//*[@id='shipping-variant-div']/div/div[2]/div[7]").text
                d_split = dispatch.split(" ")[2:]
                d_join = " ".join(d_split)
                dispatch_from = d_join
          except:
                dispatch_from = np.nan
            
          try:
                images = loaded.find_element_by_xpath("//ul[starts-with(@class, 'wt-list-unstyled wt-display-flex-xs')]")
                i_list = images.find_elements_by_xpath("//li[@class='wt-mr-xs-1 wt-mb-xs-1 wt-bg-gray wt-flex-shrink-xs-0 wt-rounded carousel-pagination-item-v2']")
                count_images = len(i_list)
          except:
                count_images = 1
          driver.close() # close the window
          driver.switch_to.window(windows_before) # switch_to the parent_window_handle
          
        except requests.exceptions.RequestException: #if anything weird happens...#
          random_sleep_except = random.uniform(240,360)
          print("I've encountered an error! I'll pause for"+str(random_sleep_except/60) + " minutes and try again \n")
          time.sleep(random_sleep_except) #sleep the script for x seconds and....#
          continue #...start the loop again from the beginning#
      
        else: #if the try-part works...#
          break #...break out of the loop#

    else: #if x amount of retries on the try-part don't work...#
        raise Exception("Something really went wrong here... I'm sorry.") #...raise an exception and stop the script# 
    
    return num_sales, num_basket, descriptions, days_to_arrival, cost_delivery, returns_accepted, dispatch_from, count_images
    
def get_main_page(driver, result, term):
    
    titles = result.find_element_by_css_selector("div > a[href]").get_attribute("title")
    
    shop_name = result.find_element_by_css_selector("p.screen-reader-only").text
    if shop_name[:2] == 'Ad':
        is_ad = 1
    else:
        is_ad = 0
    shop_names = shop_name.split(" ")[-1]
    
    try:
        star_rating = result.find_element_by_css_selector("span.screen-reader-only").text
        star_ratings = star_rating.split(" ")[0]
    except:
        star_ratings = np.nan
    
    try:
        num_review = result.find_element_by_css_selector('span.text-body-smaller.text-gray-lighter.display-inline-block.icon-b-1').text
        num_reviews = num_review.strip("()")
    except:
        num_reviews = 0
    
    prices = result.find_element_by_css_selector('span.currency-value').text
        
    try:    
        result.find_element_by_xpath("//span[@class='wt-badge wt-badge--small wt-badge--status-03']/span[2]")
        bestseller = 1
    except:
        bestseller = np.nan
    
    category = term
    
    return titles, is_ad, shop_names, star_ratings, num_reviews, prices, bestseller, category

def next_page(driver, page_counter):
    try:
        page = driver.find_element_by_xpath('//a[contains(@data-page,"{}")]'.format(page_counter))
        next_page = page.get_attribute("href")
        
        for i in range(3): # loop the try-part (i.e. opening the link) until it works, but only try it 4 times at most#
            try: #try the following:#
              random_sleep_link = 4
              time.sleep(random_sleep_link)
              driver.get(next_page) #access the URL using the header settings defined earlier#
          
            except requests.exceptions.RequestException: #if anything weird happens...#
              random_sleep_except = random.uniform(240,360)
              print("I've encountered an error! I'll pause for"+str(random_sleep_except/60) + " minutes and try again \n")
              time.sleep(random_sleep_except) #sleep the script for x seconds and....#
              continue #...start the loop again from the beginning#
          
            else: #if the try-part works...#
              break #...break out of the loop#
    
        else: #if x amount of retries on the try-part don't work...#
            raise Exception("Something really went wrong here... I'm sorry.") #...raise an exception and stop the script# 
    except:
        pass
    