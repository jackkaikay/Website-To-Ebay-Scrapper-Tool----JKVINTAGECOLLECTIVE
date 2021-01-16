from urllib.request import urlopen as uReq
import urllib
import urllib.request
from bs4 import BeautifulSoup as soup
import re
import os
import pandas as pd

#change .csv file name for other listings
df = pd.read_csv('Nineteen-Vintage.csv', encoding='latin1')



sold_items = []
x = 0
for items in df.index:
    print(sold_items)
    my_url = df['Item Url'][x]
    x = x + 1

    try:
        # Gets Webpage from url
        uClient = uReq(my_url)
        page_html = uClient.read()
        uClient.close()

        # runs URL through BS4
        page_soup = soup(page_html, 'html.parser')

        # Check if item is sold
        button = page_soup.find('button', {'class': 'btn btn--full add-to-cart'})

        if button.text == 'Sold Out':
            print('ITEM SOLD!!!!--------------------------------------------------')
            print('ITEM SOLD!!!!--------------------------------------------------')
            print(my_url)
            print('ITEM SOLD!!!!--------------------------------------------------')
            print('ITEM SOLD!!!!--------------------------------------------------')
            sold_items.append(df['Item/Page Title'][x])


        else:
             print(my_url)


    except:
        print('ITEM NOT 505!!!!--------------------------------------------------')
        print('ITEM NOT 505!!!!--------------------------------------------------')
        print(my_url)
        print('ITEM NOT 505!!!!--------------------------------------------------')
        print('ITEM NOT 505!!!!--------------------------------------------------')
        sold_items.append(df['Item/Page Title'][x])



