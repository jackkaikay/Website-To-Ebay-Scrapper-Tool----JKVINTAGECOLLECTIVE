from urllib.request import urlopen as uReq
import urllib
import urllib.request
from bs4 import BeautifulSoup as soup
import re
import os
import pandas as pd
import time



'''
Currently Scraped pages - 
https://www.taylorsthrift.com/collections/sale-items
'''

#1. Name the file (Keep 'W' if new excel / change to 'A' if adding)
Csvfile = 'Taylors-Thrith-Hoodies+Sweats.csv'
f = open(Csvfile, 'w')


##########################################################################################################
#create headers for file this will allow you to see where new appended items are (Delete header on run)###
##########################################################################################################
headers = 'Image Code,Title,Uploaded,Price,Listing Price,size,Measurements,Colour,Brand,Description,Item Url\n'
f.write(headers)



########################################
#Change this if total pages are larger##
########################################
total_pages = [1]



##########################################################################################################
#Change this to the next in line of codes to keep the images going up in number  (Also Change one below)##
##########################################################################################################


Items = 0


StoreCode = 'TT'
StoreItemNum = Items


i = Items

for pages in total_pages:
    try:

        #3.Here you select the page you want to scrape / Change 'OverallURL' for each entire page
        OverallURL = 'https://www.taylorsthrift.com/collections/sweaters-hoodies?page=' + str(pages)
        print(OverallURL)
        uClient = uReq(OverallURL)
        Overall_html = uClient.read()
        print(Overall_html)
        uClient.close()
        Overall_html = soup(Overall_html, 'html.parser')


        #This finds all the relevent links on the page
        links = Overall_html.find_all('a', { 'class': 'ProductItem__ImageWrapper ProductItem__ImageWrapper--withAlternateImage'})


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
                button = page_soup.find('button', {'class': 'ProductForm__AddToCart Button Button--secondary Button--full'})


                inDB = 0
                if inDB == 0:
                    if button.text != 'Sold Out':

                        #Grabs each image
                        #Select title and draw all images from site.

                        pagetitle = page_soup.h1.text
                        brand = page_soup.h2.text
                        print(brand)





                        #Searches whole description and breaks up into paragraphs
                        paragraphs = page_soup.findAll('p', {'class':'p1'})

                        #Pull paragraphs from page
                        size = paragraphs[0].text
                        Measurements = paragraphs[2].text
                        Colour = paragraphs[3].text

                        para1 = paragraphs[0].text
                        para2 = paragraphs[1].text
                        para3 = paragraphs[2].text
                        para4 = paragraphs[3].text
                        para5 = paragraphs[4].text
                        #Remove and sort strings before excell placement

                        size = size.replace(',','|')
                        size = size.replace('Size on label:', '')

                        Measurements = Measurements.replace(',','/')

                        Colour = Colour.replace(',','')
                        Colour = Colour.replace('Colour:', '')
                        Colour = Colour.replace('|', '/')



                        pagetitle = pagetitle.replace('/','-')
                        pagetitle = pagetitle.replace('~', '-')
                        pagetitle = pagetitle.replace('Vintage', '')
                        pagetitle = pagetitle.replace('VINTAGE', '')
                        pagetitle = pagetitle.replace('-', '/')
                        pagetitle = pagetitle.replace('~', '/')
                        pagetitle = pagetitle.split("_", 1)

                        print('final123')
                        # Error traps if the item is on sale or not. Draws the lowest price
                        price = page_soup.find('span', { 'class': 'ProductMeta__Price Price Price--highlight Text--subdued u-h4'}).text if page_soup.find('span', {'class': 'ProductMeta__Price Price Price--highlight Text--subdued u-h4'}) else ''
                        if price == '':
                            print('NOT ON SALE')
                            price = page_soup.find('span', {'class': 'ProductMeta__Price Price Text--subdued u-h4'}).text

                        #Price Algorithm
                        #Remove Pound Sign
                        Listing_price = price[1:]

                        Listing_price = float(Listing_price)
                        print(Listing_price)
                        if Listing_price < 10:
                            Listing_price_final = Listing_price * 1.7
                            Listing_price_final = Listing_price_final + 3.50
                            print(str(Listing_price_final))
                        if Listing_price > 10 and Listing_price < 20:
                            Listing_price_final = Listing_price * 1.6
                            Listing_price_final = Listing_price_final + 3.50
                            print(str(Listing_price_final))
                        if Listing_price >= 20 and Listing_price < 30:
                            Listing_price_final = Listing_price * 1.5
                            Listing_price_final = Listing_price_final + 3.50
                            print(str(Listing_price_final))
                        if Listing_price >= 30 and Listing_price < 40:
                            Listing_price_final = Listing_price * 1.45
                            Listing_price_final = Listing_price_final + 3.50
                            print(str(Listing_price_final))
                        if Listing_price >= 40 and Listing_price < 50:
                            Listing_price_final = Listing_price * 1.45
                            Listing_price_final = Listing_price_final + 3.50
                            print(str(Listing_price_final))
                        if Listing_price >= 50 and Listing_price < 60:
                            Listing_price_final = Listing_price * 1.4

                            print(str(Listing_price_final))
                        if Listing_price >= 60 and Listing_price < 70:
                            Listing_price_final = Listing_price * 1.35
                            print(str(Listing_price_final))
                        if Listing_price >= 70:
                            Listing_price_final = Listing_price * 1.3
                            print(str(Listing_price_final))

                        # Write output to CSV

                        print(str(pagetitle))
                        StoreItemNum = StoreItemNum + 1
                        f.write(str(StoreItemNum) + StoreCode + "," + pagetitle[0] + " / " + size + " / " + Colour  + "," + "FALSE" + "," + price + "," + str(Listing_price_final) + "," + size + "," + Measurements + "," + Colour + ","  + brand + "," + para1 + '<br>' + para2 + '<br>' + para3 + '<br>' + para4 + '<br>' + para5 + "," + my_url + '\n')

                    else:
                        print('Sold Out Item')
                else:
                    print('Item In Database')
            except:
                print('same name found twice')
    except:
        print('Pagination Fucked')

f.close
