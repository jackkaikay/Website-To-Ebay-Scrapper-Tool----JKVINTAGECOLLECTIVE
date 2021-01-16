from urllib.request import urlopen as uReq
import urllib
import urllib.request
from bs4 import BeautifulSoup as soup
import re
import os
import pandas as pd
import time

#https://nineteenvintage.com//collections/all-products/products/checked-nautica-shirt-xl
#https://nineteenvintage.com//collections/all-products/products/checked-chaps-shirt-xl-11
# setting the new direct link to the item page
my_url = 'https://nineteenvintage.com//collections/all-products/products/tommy-hilfiger-outdoors-short-sleeve-shirt-xs'

# Gets Webpage from url
uClient = uReq(my_url)
page_html = uClient.read()
uClient.close()

# runs URL through BS4
page_soup = soup(page_html, 'html.parser')

print(my_url)

# Add sold checker
button = page_soup.find('button', {'class': 'btn btn--full add-to-cart'})
button = button.text.strip()




item_name = page_soup.find('h1', {'class': 'h2 product-single__title'}).text
price = page_soup.find('span', {'class': 'money'}).text
paragraphs = page_soup.findAll('tr')
print('1')

print(paragraphs)

brand = paragraphs[0].text
colour = paragraphs[1].text
condition = paragraphs[2].text
size = paragraphs[3].text
pit_pit = paragraphs[4].text
shoulder_waist = paragraphs[5].text
shoulder_cuff = paragraphs[6].text

print('2')


brand = brand[7:]
colour = colour[8:]
condition = condition[10:]
size = size[8:]
pit_pit = pit_pit[20:]
shoulder_waist = shoulder_waist[27:]
shoulder_cuff = shoulder_cuff[26:]



brand = brand.strip()
colour = colour.strip()
condition = condition.strip()
size = size.strip()
pit_pit = pit_pit.strip()
shoulder_waist = shoulder_waist.strip()
shoulder_cuff = shoulder_cuff.strip()


print(brand)
print(colour)
print(condition)
print(size)
print(pit_pit)
print(shoulder_waist)
print(shoulder_cuff)




