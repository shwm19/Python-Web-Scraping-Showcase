# -*- coding: utf-8 -*-
"""
Created on Sat Dec 11 14:38:23 2021

@author: shwm19


Retrieve number of reviews for products on the page.  AWS Best Sellers
Put into a Dataframe

TODO: 
Add Product Names and Categories
Add Ability to specify Category
Add abilitity to specify multiple categories
Add ability UI
Add ability to manipulate timer from UI

"""

class Not200OK(Exception):
    """You did not get a 200 OK Response"""
    def __init__ (self, status_code, message="You did not get a 200 OK Response"):
        self.status_code = status_code
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.status_code} -> {self.message}'


import requests
from bs4 import BeautifulSoup
import pandas as pd
import time


url = "https://www.amazon.com/Best-Sellers/zgbs"
headers = {"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36","encoding":""}


def review_count_scrape():
    r = getScrapedData()
    soup = BeautifulSoup(r.content, 'lxml' )
    product_review_counts = [i.find("span",class_="a-size-small").text for i in soup.find_all("div",class_="a-icon-row")]
    # Need to find a way to abstract htis so it's not a magic string of some sort
    df = pd.DataFrame(product_review_counts)
    print(df) #Prints the dataframe for now.
    
    #add timer
    time.sleep(60)


def getScrapedData(): #Responsible for grabbing the data.
    r = requests.get(url, headers = headers)
    if r.status_code == 200: #Validate we got a 200
        return r
    else: 
        raise Not200OK(r.status_code)

def main():    
    end_timer= time.time() +60 * 2 #Allow run twice
    while time.time() < end_timer:
        review_count_scrape()   

if __name__ == "__main__":
    main()