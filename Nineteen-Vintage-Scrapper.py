from urllib.request import urlopen as uReq
import urllib
import urllib.request
from bs4 import BeautifulSoup as soup
import re
import os
import pandas as pd
import time


total_pages = [1,2,3,4,5,6,7]


Code = 0
Store = 'NV'


y = Code


Csvfile = 'Nineteen-Vintage-Inventory.csv'
f = open(Csvfile, 'w')
headers = 'Image Code,Uploaded,Item/Page Title,Price,Listing Price,colour,Size,Condition,Brand,Description,Imageurls,Item Url\n'
f.write(headers)


for pages in total_pages:
    try:

        #3.Here you select the page you want to scrape / Change 'OverallURL' for each entire page
        OverallURL = 'https://nineteenvintage.com/collections/all-products?page=' + str(pages)
        uClient = uReq(OverallURL)
        Overall_html = uClient.read()
        uClient.close()
        Overall_html = soup(Overall_html, 'html.parser')


        #This finds all the relevent links on the page
        links = Overall_html.find_all('div', { 'class': 'grid-product__content'})

        for link in links:
            try:



                link = link.a['href']

                #setting the new direct link to the item page
                my_url = 'https://nineteenvintage.com/' + link

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
                if button != 'Sold Out':

                    try:



                        item_name = page_soup.find('h1', {'class': 'h2 product-single__title'}).text
                        price = page_soup.find('span', {'class': 'money'}).text
                        paragraphs = page_soup.findAll('td', {'data-mce-fragment':'1'})

                        brand = paragraphs[1].text
                        colour = paragraphs[3].text
                        condition = paragraphs[5].text
                        sizing = paragraphs[7].text
                        pit_pit = paragraphs[9].text
                        shoulder_waist = paragraphs[11].text
                        shoulder_cuff = paragraphs[13].text

                        y = y + 1


                        brand = brand.replace(',','')
                        colour = colour.replace(',','')
                        condition = condition.replace(',','')
                        sizing = sizing.replace(',','')
                        pit_pit = pit_pit.replace(',','')
                        shoulder_waist = shoulder_waist.replace(',','')
                        shoulder_cuff = shoulder_cuff.replace(',','')

                        brand = brand.strip()
                        colour = colour.strip()
                        condition = condition.strip()
                        sizing = sizing.strip()
                        pit_pit = pit_pit.strip()
                        shoulder_waist = shoulder_waist.strip()
                        shoulder_cuff = shoulder_cuff.strip()






                        Listing_price = price[1:]
                        price = price[1:]
                        item_name = item_name.strip()




                        Listing_price = float(Listing_price)

                        if Listing_price < 10:
                            Listing_price_final = Listing_price * 1.7
                            Listing_price_final = Listing_price_final + 3.50
                            print(str(Listing_price_final))
                        if Listing_price >= 10 and Listing_price < 20:
                            Listing_price_final = Listing_price * 1.55
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

                        print('check')

                        p = 0
                        urllist = []
                        for Image in page_soup.findAll('img'):

                            temp = Image.get('data-photoswipe-src') if Image.get('data-photoswipe-src') else ''
                            print(temp)
                            imageURL = temp[2:]

                            imageURL = imageURL.replace('900x.', '1280x.')
                            imageURL = imageURL.replace('620x.', '1280x.')

                            urllist.append(imageURL)

                            p = p + 1
                            if p == 7:
                                break





                        item_name = item_name.replace(',', '')
                        colour = colour.strip()
                        urllist = '|'.join(urllist)
                        urllist = urllist.replace('|||', '')
                        urllist = urllist[:-1]

                        f.write(item_name + " / " + colour + " / " + Store + str(y) + "," + "FALSE" + "," + Store  + str(y) +"," + price + "," + str(Listing_price_final) + "," + str(colour) + "," + str(sizing) + "," + str(condition) + "," + brand + "," + item_name + " / " + colour + '<br>' + 'Pit to Pit (Inches): ' + pit_pit + '<br> Shoulder to Waist (Inches): '  + shoulder_waist + '<br> Shoulder to Cuff (Inches): ' + shoulder_cuff  + '<br>' + sizing + "," + urllist + ',' +  my_url + '\n')




                    except:

                        y = y + 1

                        item_name = page_soup.find('h1', {'class': 'h2 product-single__title'}).text
                        price = page_soup.find('span', {'class': 'money'}).text
                        paragraphs = page_soup.findAll('tr')

                        brand = paragraphs[0].text
                        colour = paragraphs[1].text
                        condition = paragraphs[2].text
                        size = paragraphs[3].text
                        pit_pit = paragraphs[4].text
                        shoulder_waist = paragraphs[5].text
                        shoulder_cuff = paragraphs[6].text

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

                        brand = brand.replace(',','')
                        colour = colour.replace(',','')
                        condition = condition.replace(',','')
                        size = size.replace(',','')
                        pit_pit = pit_pit.replace(',','')
                        shoulder_waist = shoulder_waist.replace(',','')
                        shoulder_cuff = shoulder_cuff.replace(',','')





                        Listing_price = price[1:]
                        price = price[1:]
                        item_name = item_name.strip()

                        Listing_price = float(Listing_price)

                        if Listing_price < 10:
                            Listing_price_final = Listing_price * 1.7
                            Listing_price_final = Listing_price_final + 3.50
                            print(str(Listing_price_final))
                        if Listing_price >= 10 and Listing_price < 20:
                            Listing_price_final = Listing_price * 1.55
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




                        p = 0
                        urllist = []
                        for Image in page_soup.findAll('img'):

                            temp = Image.get('data-photoswipe-src') if Image.get('data-photoswipe-src') else ''
                            print(temp)
                            imageURL = temp[2:]

                            imageURL = imageURL.replace('900x.', '1280x.')
                            imageURL = imageURL.replace('620x.', '1280x.')

                            urllist.append(imageURL)

                            p = p + 1
                            if p == 7:
                                break



                        item_name = item_name.replace(',', '')
                        colour = colour.strip()
                        urllist = '|'.join(urllist)
                        urllist = urllist.replace('|||', '')
                        urllist = urllist[:-1]

                        f.write(item_name + " / " + colour + " / " + Store + str(y) + "," + "FALSE" + "," + Store + str(y) + "," + price + "," + str(Listing_price_final) + "," + str(colour) + "," + str(size) + "," + str(condition) + "," + brand + "," + item_name + " / " + colour + '<br>' + 'Pit to Pit (Inches): ' + pit_pit + '<br> Shoulder to Waist (Inches): '  + shoulder_waist + '<br> Shoulder to Cuff (Inches): ' + shoulder_cuff + '<br>' + size +  "," + urllist + ',' +  my_url + '\n')



                else:
                    print('blah1')
            except:
                print('blah2')
        else:
            print('bash3')
    except:
        print('blah4')
