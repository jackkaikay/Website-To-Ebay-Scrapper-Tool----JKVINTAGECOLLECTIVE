from urllib.request import urlopen as uReq
import urllib
import urllib.request
from bs4 import BeautifulSoup as soup
import re
import os
import pandas as pd
import time

#1. The current stock inventory assosiated with the store.
df = pd.read_csv('Taylors-Thrith.csv', encoding='latin1')


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
headers = 'Image Code,Uploaded,Item/Page Title,Price,Listing Price,size,Measurements,Colour,Item Url\n'
f.write(headers)



########################################
#Change this if total pages are larger##
########################################
total_pages = [1,2]



##########################################################################################################
#Change this to the next in line of codes to keep the images going up in number  (Also Change one below)##
##########################################################################################################
########################################
#Change this if total pages are larger##
########################################
Items = 0



y = Items
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

                # Need to add a check if the items allready in my database
                inDB = df['Item Url'].str.contains(my_url).sum()
                if inDB == 0:
                    if button.text != 'Sold Out':

                        #Grabs each image
                        #Select title and draw all images from site.

                        pagetitle = page_soup.h1.text

                        # Create Directory for the image

                        y = y + 1
                        directory = str(y) + ' ' + pagetitle.replace('/','-')
                        print(directory)
                        parent_dir = 'C:/Users/jackk/Desktop/GITHUB/EbayScraper/Downloaded Images Taylors Thrith/'
                        path = os.path.join(parent_dir, directory)
                        os.mkdir(path)
                        print(path)


                        for Image in page_soup.findAll('img'):
                            temp = Image.get('data-original-src') if Image.get('data-original-src') else ''

                            if temp != '':
                                if temp != '//cdn.shopify.com/s/files/1/0380/3099/9685/files/TT_Logo_Palm_350x.jpg?v=1599171923':
                                    #Makes file name add number to end
                                    filename =  pagetitle + '_' + str(i)
                                    filename = filename.replace('/','-')
                                    filename = filename.replace('Vintage', '')
                                    i = i + 1
                                    temp = temp[2:]
                                    temp = 'https://' + temp

                                    # Writing the image
                                    imageFile = open(path + '/' + str(y) + ' ' +filename + ".png", 'wb')
                                    print(temp)
                                    imageFile.write(urllib.request.urlopen(temp).read())
                                    imageFile.close()
                                else:
                                    print('Logo Image')
                            else:
                                print('')


                        #Searches whole description and breaks up into paragraphs
                        paragraphs = page_soup.findAll('p', {'class':'p1'})

                        #Pull paragraphs from page
                        size = paragraphs[0].text
                        Measurements = paragraphs[2].text
                        Colour = paragraphs[3].text



                        #Remove and sort strings before excell placement

                        size = size.replace(',','|')
                        size = size.replace('Size on label:', '')

                        Measurements = Measurements.replace(',','/')

                        Colour = Colour.replace(',','')
                        Colour = Colour.replace('Colour:', '')
                        Colour = Colour.replace('|', '/')



                        pagetitle = pagetitle.replace('/','-')
                        pagetitle = pagetitle.replace('~', '-')
                        pagetitle = filename = filename.replace('Vintage', '')

                        pagetitle = pagetitle.replace('-', '/')
                        pagetitle = pagetitle.replace('~', '/')
                        pagetitle = pagetitle.split("_", 1)



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
                        print()
                        Imagecode = str(y)
                        print(Imagecode)


                        print(str(pagetitle))
                        f.write(pagetitle[0] + " / " + size + " / " + Colour +  " / " + Imagecode + "," + "FALSE" + "," + str(Imagecode) + "," + price + "," + str(Listing_price_final) + "," + size + "," + Measurements + "," + Colour + ","  + my_url + '\n')

                    else:
                        print('Sold Out Item')
                else:
                    print('Item In Database')
            except:
                print('same name found twice')
    except:
        print('Pagination Fucked')

f.close
