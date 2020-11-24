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
import time 
import re 

import pandas as pd 
import numpy as np 

def get_url_list(search_list):
    url_list = []
    for term in search_list:
        url_list.append('https://www.etsy.com/uk/search?q=' + re.sub("\s", "+", term))
    return url_list
    
def close_popup(driver):
    pop_up_xpath = "//*[@id='gdpr-single-choice-overlay']/div/div[2]/div[2]/button"
    try:
        driver.find_element_by_xpath(pop_up_xpath).click()
        time.sleep(2)
    except:
        pass
    
def open_page(driver, URL):
    driver.get(URL)
    time.sleep(4)
    close_popup(driver)
    