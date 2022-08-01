# -*- coding: utf-8 -*-
"""
Created on Sat Dec 11 14:38:23 2021

@author: shwm19


Retrieve number of reviews for products on the page.  AWS Best Sellers
Put into a Dataframe

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

class AmazonScraper:


    def __init__(self, url = "https://www.amazon.com/Best-Sellers/zgbs" , 
    headers = {"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36","encoding":""} ):
        self.url = url
        self.headers = headers


    def scrapeData(self): #Responsible for grabbing the data.
        self.r = requests.get(self.url, headers = self.headers)
        if self.r.status_code != 200: #Validate we got a 200
            raise Not200OK(self.r.status_code)


    def bestSellerNamesAndNumReviews(self):
        soup = BeautifulSoup(self.r.content, 'lxml' )
        product_review_counts =[]
        divs_to_parse = [i for i in soup.find_all("li",class_="a-carousel-card")]
        data = {"name": [],  "rating": [], "price": []  }
        for div in divs_to_parse:
            data['name'].append( div.find("img",alt=True, class_="a-dynamic-image")["alt"])
            data['rating'].append( div.find("span",class_="a-icon-alt").text)
            data['price'].append( div.find("span",class_="a-size-base").text)
        pd.set_option('display.max_colwidth', None)
        df = pd.DataFrame(data)
        print(df)
        self.debugOutput()


    def debugOutput(self):
        with open("debug.html" , "w",  encoding="utf-8") as dl:
            dl.write(self.r.text)

# END CLASS
def main():    ## Example of a run and usecase. This could be imported 
    timeToWait = 60 #Time in seconds to wait
    end_timer= time.time() +timeToWait * 2 #Allow run twice
    amazon_scraper = AmazonScraper()
    while time.time() < end_timer:
        amazon_scraper.scrapeData() # Scrape the data This allows us to cache the result should we so choose. 
        #amazon_scraper.review_count_scrape()   
        amazon_scraper.bestSellerNamesAndNumReviews()
        #add timer
        time.sleep(timeToWait)

if __name__ == "__main__": #If you run the module you'll run a test of a couple functions. 
    main()