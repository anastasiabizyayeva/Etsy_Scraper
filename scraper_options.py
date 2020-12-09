# -*- coding: utf-8 -*-
"""
Created on Tue Nov 24 15:03:54 2020

@author: Anastasia
"""
# Set local path of chromedriver
PATH = "C:/Program Files (x86)\chromedriver.exe"

#Input the search terms you want to look up 
search_terms = ['nerdy greeting card', 'birthday card', 'congratulations card']

#Choose how many pages of each search term you want to scrape. Note that Etsy has a limit of 240 pages of search results for anything you look up, so that's the default here. 
page_counter_limit = 240
