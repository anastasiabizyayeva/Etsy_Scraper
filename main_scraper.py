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

#Establish path to Chromedriver

PATH = "C:/Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)

#Establish connection to URL

URL = "https://www.etsy.com/uk/search?q=birthday%20card"

driver.get(URL)

#Check if the listing is an add - have a column for this. Starts with 'Ad by' 

#From base page scrape title, shop name, star rating, how many stars, price, whether there's free UK delivery, whether bestseller, whether discounted 

#From click in, scrape 1- local seller, 2-num sales, 3-'other people want this', 4-description, 5- estimated arrival, 6- cost to deliver, 7-whether returns are accepted, 8-where it dispatches from, 9-count of images 

driver.quit()


