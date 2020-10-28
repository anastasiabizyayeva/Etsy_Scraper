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


#Loop through the scraping code until we get 6000 records

while record_counter < 10:
    
    #Ensure main search results populate before further action is taken

    try:
        main = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'bg-white display-blick pb-xs-2 mt-xs-0')))

    
        #Get the listing containers and loop through them
        
        print('test')
        
        results = main.find_elements_by_class_name("wt-list-unstyled wt-grid__item-xs-6 wt-grid__item-md-4 wt-grid__item-lg-3 wt-order-xs-0 wt-order-sm-0 wt-order-md-0 wt-order-lg-0 wt-order-xl-0 wt-order-tv-0 grid__item-xl-fifth tab-reorder")
        
        for result in results:
            print(len(result))
        #Loop over each vacancy 
    
        # for result in results:
                    
        #     #Get title
            
        #     title = result.find_element_by_css_selector("h2 > a[href]").get_attribute("title")
        #     titles.append(title)  
            
        #     #Get department
            
        #     department = result.find_element_by_tag_name("h3").text
        #     departments.append(department)
            
        #     #Get salary info 
            
        #     salary = result.find_element_by_class_name('salary')
        #     salaries.append(salary.text)
            
        #     #Get location info
                   
        #     employer = result.find_element_by_class_name('agency')
        #     employers.append(employer.text)
        
        # #Initialize an empty list to hold links to each job search result 
        
        # link_list = []
        
        # #Find links for each job posted and append them to our links list 
        
        # links = driver.find_elements_by_css_selector("h2 > a[href]")
        
        # for link in links:
        #     link_text = link.get_attribute("href")
        #     link_list.append(link_text)
        
        # #Loop over links and get pertinent information
            
        # for link in link_list:
        #     driver.get(link)
            
        #     #Get job type 
            
        #     j_type = driver.find_elements_by_xpath("//dt[.='Job Type:']/following-sibling::dd[1]")
        #     if not j_type: x = "None"
        #     else: x = j_type[0].text
        #     job_types.append(x)
            
        #     #Get working pattern
            
        #     w_pattern = driver.find_elements_by_xpath("//dt[.='Working pattern:']/following-sibling::dd[1]")
        #     if not w_pattern: x = "None"
        #     else: x = w_pattern[0].text
        #     working_patterns.append(x)
            
        #     #Get pay scheme
            
        #     p_scheme = driver.find_elements_by_xpath("//dt[.='Pay Scheme:']/following-sibling::dd[1]")
        #     if not p_scheme: x = "None"
        #     else: x = p_scheme[0].text
        #     pay_schemes.append(x)
            
        #     #Get pay band
            
        #     p_band = driver.find_elements_by_xpath("//dt[.='Pay Band:']/following-sibling::dd[1]")
        #     if not p_band: x = "None"
        #     else: x = p_band[0].text
        #     pay_bands.append(x)
             
        #     #Get location
            
        #     location = driver.find_elements_by_xpath("//dt[.='Location:']/following-sibling::dd[1]")
        #     if not location: x = "None"
        #     else: x = location[0].text
        #     locations.append(x)
            
        #     #Get description
            
        #     description = driver.find_elements_by_xpath("/html/body/div[2]/div[3]/div/div/div/div/div[1]/div[2]/div[3]")
        #     if not description: x = "None"
        #     else: x = description[0].text
        #     descriptions.append(x)
            
        #     #Go back to previous page 
            
        #     driver.back()
            
        #     #Add 1 to page counter- there should be 20 results scraped before the next page is accessed
            
        #     page_counter += 1
        
        # if page_counter == 20:
            
        #     #Get job ref 
            
        #     j_ref = driver.find_elements_by_xpath("//dt[.='Job Ref:']/following-sibling::dd")
        #     for x in j_ref:
        #         job_ref.append(x.text)
            
        #     #Get posted date
            
        #     posted_date = driver.find_elements_by_xpath("//dt[.='Posted:']/following-sibling::dd")
        #     for x in posted_date:
        #         posted_dates.append(x.text)
            
        #     #Get closing date 
            
        #     closing_date = driver.find_elements_by_xpath("//dt[.='Closing Date:']/following-sibling::dd")
        #     for x in closing_date:
        #         closing_dates.append(x.text)
            
        #     #Print out page counter to ensure there are 20 results scraped from every apge 

        #     print('Page Counter:' + str(page_counter))
            
        #     #Add 20 records to our overall record count, then reset page counter in anticipation of us clicking onto the next page 
            
        #     record_counter += 20
        #     page_counter = 0
            
        #     #Print out our total records scraped, whether there's a value for each row, and how many pages we've scraped from the search results.
            
        #     print('Record Counter:' + str(record_counter))
        #     print(len(employers) == record_counter)
        #     print('Page ' + str(int(record_counter/20)) + ' scraping complete.')
            
        #     #Ensuring we're clicking on the right link to get to the next page - there are 3 separate ways its formatted across the search 
            
        #     if record_counter == 20:
        #         num = 0
        #     elif record_counter >= 120:
        #         num = 6
        #     else:
        #         num = (record_counter/20)
                
        #     #Find and click on next link 
            
        #     next_page = driver.find_element_by_xpath("//ul[@class='pagination']//li[{}]".format(2+num))
        #     next_page.click()

    except:
        break

#Exit browser

driver.quit()

#Create dictionaries from our lists 

# data = {}

#Create dataframe from our dictionary  
            
# df = pd.DataFrame(data)

#Save dataframe to a new CSV 

# df.to_csv('raw_data.csv', index=False)
