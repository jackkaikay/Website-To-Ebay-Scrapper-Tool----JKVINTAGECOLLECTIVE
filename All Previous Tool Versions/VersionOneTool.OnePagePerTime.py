from urllib.request import urlopen as uReq
import urllib
import urllib.request
from bs4 import BeautifulSoup as soup
import re
import os

#Open the file
Csvfile = 'listingsTEST.csv'
f = open(Csvfile, 'w')


#create headers for file
headers = 'Item/Page Title,Price,Listing Price,size, Reccomended Size, Measurements,Colour,Condition,Description_1,Description_2 \n'
f.write(headers)

#Here you select the page you want to scrape
OverallURL = 'https://www.taylorsthrift.com/collections/lacoste/products/vintage-lacoste-polo-shirt-medium'
uClient = uReq(OverallURL)
Overall_html = uClient.read()
uClient.close()
Overall_html = soup(Overall_html, 'html.parser')


button = Overall_html.find('button', { 'class': 'ProductForm__AddToCart Button Button--secondary Button--full'})
print(button.text)




def vintagePage():
    #my_url = 'https://www.taylorsthrift.com/collections/lacoste/products/vintage-lacoste-polo-shirt-medium'
    my_url = 'https://www.taylorsthrift.com//collections/sale-items/products/rare-80s-adidas-adi-tex-jacket'


    #Gets Webpage from url
    uClient = uReq(my_url)
    page_html = uClient.read()
    uClient.close()

    #runs URL through BS4
    page_soup = soup(page_html, 'html.parser')


    #Grabs each image
    #Select title and draw all images from site.
    i = 1
    pagetitle = page_soup.h1.text

    '''
    for Image in page_soup.findAll('img'):
        temp = Image.get('data-original-src') if Image.get('data-original-src') else ''

        if temp != '':
            if temp != '//cdn.shopify.com/s/files/1/0380/3099/9685/files/TT_Logo_Palm_350x.jpg?v=1599171923':
                #Makes file name add number to end
                filename = pagetitle + '_' + str(i)
                i = i + 1
                temp = temp[2:]
                temp = 'https://' + temp

                #Writing the image
                imageFile = open(filename + ".png", 'wb')
                print(temp)
                imageFile.write(urllib.request.urlopen(temp).read())
                imageFile.close()
            else:
                print('Logo Image')
        else:
            print('Bad Link')
    '''

    #Searches whole description and breaks up into paragraphs
    paragraphs = page_soup.findAll('p', {'class':'p1'})


    Reccomended_size = paragraphs[0].text
    Measurements = paragraphs[1].text
    Colour = paragraphs[2].text
    Condition = paragraphs[3].text
    Description_1 = paragraphs[4].text
    Description_2 = paragraphs[5].text


    Reccomended_size.replace(',','|')
    Measurements = Measurements.replace(',','|')
    Colour = Colour.replace(',','|')
    Condition = Condition.replace(',','|')
    Description_1.replace(',','|')
    Description_2.replace(',','|')

    print(Measurements)
    print(Colour)
    print(Condition)

    # Error traps if the item is on sale or not. Draws the lowest price
    price = page_soup.find('span', { 'class': 'ProductMeta__Price Price Price--highlight Text--subdued u-h4'}).text if page_soup.find('span', {'class': 'ProductMeta__Price Price Price--highlight Text--subdued u-h4'}) else ''
    if price == '':
        print('NOT ON SALE')
        price = page_soup.find('span', {'class': 'ProductMeta__Price Price Text--subdued u-h4'}).text

    #Price Algorithm
    Listing_price = price[1:]
    Listing_price = float(Listing_price)
    print(Listing_price)
    if Listing_price < 10:
        Listing_price_final = Listing_price * 1.7
        print(str(Listing_price_final))
    if Listing_price > 10 and Listing_price < 20:
        Listing_price_final = Listing_price * 1.6
        print(str(Listing_price_final))
    if Listing_price > 20 and Listing_price < 30:
        Listing_price_final = Listing_price * 1.5
        print(str(Listing_price_final))
    if Listing_price > 30 and Listing_price < 40:
        Listing_price_final = Listing_price * 1.45
        print(str(Listing_price_final))
    if Listing_price > 40 and Listing_price < 50:
        Listing_price_final = Listing_price * 1.45
        print(str(Listing_price_final))
    if Listing_price > 50 and Listing_price < 60:
        Listing_price_final = Listing_price * 1.4
        print(str(Listing_price_final))
    if Listing_price > 60 and Listing_price < 70:
        Listing_price_final = Listing_price * 1.35
        print(str(Listing_price_final))
    if Listing_price > 70:
        Listing_price_final = Listing_price * 1.3
        print(str(Listing_price_final))

    '''
    if Listing_price in range (0,10):
        Listing_price_final = Listing_price * 1.70
        Freeshipping = 'No'
    if Listing_price in range (10,20):
        Listing_price_final = Listing_price * 1.60
        Freeshipping = 'No'
    if Listing_price in range (20,30):
        Listing_price_final = Listing_price * 1.50
        Freeshipping = 'No'
    if Listing_price in range (30,40):
        Listing_price_final = Listing_price * 1.45
        Freeshipping = 'No'
    if Listing_price in range (40,50):
        Listing_price_final = Listing_price * 1.45
        Freeshipping = 'No'
    if Listing_price in range (50,60):
        Listing_price_final = Listing_price * 1.40
        Freeshipping = 'Yes'
    if Listing_price in range (60,70):
        Listing_price_final = Listing_price * 1.35
        Freeshipping = 'Yes'
    if Listing_price in range (70,1000):
        Listing_price_final = Listing_price * 1.3
        Freeshipping = 'Yes'
    '''



    # Write output to CSV
    print()
    f.write(pagetitle + "," + price + "," + str(Listing_price_final) + "," + Reccomended_size + "," + Measurements + "," + Colour + "," + Condition + "," + Description_1 + "," + Description_2 + '\n')
    f.close


vintagePage()