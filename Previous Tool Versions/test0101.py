from urllib.request import urlopen as uReq
import urllib
import urllib.request
from bs4 import BeautifulSoup as soup
import re
import os
import pandas as pd



df = pd.read_csv('listings.csv', encoding='latin1')


'''
Currently Scraped pages - 
https://www.taylorsthrift.com/collections/sale-items

'''

#1. Name the file (Keep 'W' if new excel / change to 'A' if adding)
Csvfile = 'listings.csv'
f = open(Csvfile, 'a')

#create headers for file
headers = 'Image Code,Item/Page Title,Price,Listing Price,Free Shipping, size,Reccomended Size,Measurements,Colour,Condition,Item Url\n'
#2. Remove this write if appending data / Keep in for new list
#f.write(headers)

#3.Here you select the page you want to scrape / Change 'OverallURL' for each entire page (If page has multiple pages you will need to re add link
OverallURL = 'https://www.taylorsthrift.com/collections/sale-items'
uClient = uReq(OverallURL)
Overall_html = uClient.read()
uClient.close()
Overall_html = soup(Overall_html, 'html.parser')
#4. no other alterations needed



#This finds all the relevent links on the page
links = Overall_html.find_all('a', { 'class': 'ProductItem__ImageWrapper ProductItem__ImageWrapper--withAlternateImage'})


xx = 0
y = 0
Iterator = 0
for link in links:
    try:
        #Looping through all items on page
        item_page = str(links[Iterator]['href'])
        Iterator = Iterator + 1

        #setting the new direct link to the item page
        my_url = 'https://www.taylorsthrift.com/' + item_page


        #Gets Webpage from url
        uClient = uReq(my_url)
        page_html = uClient.read()
        uClient.close()

        #runs URL through BS4
        page_soup = soup(page_html, 'html.parser')

        #Check if item is sold
        print(my_url)


        # Need to add a check if the items allready in my database
        print('pre loop')
        inDB = df['Item Url'].str.contains(my_url).sum()
        print(inDB)
        if inDB == 0:
            print('Scrape it')
        else:
            print('dont')
    except:
        print('same name found twice')

f.close
