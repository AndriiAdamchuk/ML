#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 31 18:00:47 2020

@author: andrii
"""


from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium import webdriver
##from selenium.webdriver.common.keys import Keys
import time
import pandas as pd

def get_apartments(city, num_apartments, verbose):
##Running webdriver
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(executable_path='/Users/andrii/Documents/ds_proj/chromedriver', options=options)
    driver.set_window_size(1120, 1000)
    url = 'https://www.thelocal.de/rentals/' + city +'?&page=1'
    driver.get(url)
    apartments = []
    
    while len(apartments) < num_apartments:
        time.sleep(4)

        apartment_buttons = driver.find_elements_by_class_name('Pagination-item Pagination-next')

        for apartment_buttons in apartment_buttons:
            
            print("Progress: {}".format("" + str(len(apartments)) + "/" + str(num_apartments)))
            if len(apartments) >= num_apartments:
                break        
            
            apartment_buttons.click()  #You might 
            time.sleep(3)
            collected_successfully = False
            
            while not collected_successfully:
                try:       
                    apartment_title = driver.find_elements_by_class_name('Listing-descriptionTitle').text
                    price_per_month = driver.find_elements_by_class_name('ListingPrice-price').text
                    rooms = driver.find_elements_by_class_name('ListingDetailsBrief-rooms').text
                    beds = driver.find_elements_by_class_name('ListingDetailsBrief-beds').text
                    area = driver.find_elements_by_class_name('ListingDetailsBrief-area').text
                    collected_successfully = True
                except:
                    time.sleep(5)

            if verbose:
                print("Title: {}".format(apartment_title[:500]))
                print("Price: {}".format(price_per_month))
                print("Rooms: {}".format(rooms))
                print("Beds: {}".format(beds))
                print("Area: {}".format(area))
                
                
            apartments.append({"Title" : apartment_title, "Price" : price_per_month, "Rooms" : rooms, "Beds" : beds, "Area" : area})
            #add job to apartments
        
        try:
             driver.find_element_by_xpath('.//a[@class="Pagination-item Pagination-next"]//a').click()
        except NoSuchElementException:     
            print("Scraping terminated before reaching target number of apartments. Needed {}, got {}.".format(num_apartments, len(apartments)))
            break

    return pd.DataFrame(apartments)

df = get_apartments('berlin', 15, False)
df