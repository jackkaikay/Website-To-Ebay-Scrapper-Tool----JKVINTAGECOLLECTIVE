from os import system, mkdir
import concurrent.futures
import multiprocessing

from time import sleep
from time import time
from datetime import datetime
import re


try:
    from selenium import webdriver
    from webdriver_manager.chrome import ChromeDriverManager
    import pandas
    import requests
    from bs4 import BeautifulSoup
except ModuleNotFoundError:
    system("pip install -r requirements.txt")
    from selenium import webdriver
    from webdriver_manager.chrome import ChromeDriverManager
    import pandas
    import requests
    from bs4 import BeautifulSoup


def get_selenium_driver():
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    #driver = webdriver.Chrome()

    driver.delete_all_cookies()
    driver.maximize_window()
    return driver


def get_soup(html_text):
    return BeautifulSoup(html_text, 'html.parser')


def prepare_soup(link):
    html = requests.get(link)
    if html.status_code == 200:
        return BeautifulSoup(html.text, "html.parser")
    else:
        return False

def remove_html_tags_keeping_one_tag(string,tags_to_keep,replace_by):
    string = string.strip().replace("\n",'')
    while True:
        tag = re.search(r"<(\"[^\"]*\"|'[^']*'|[^'\">])*>",string)
        if tag:
            tag = tag.group()
            if tag in tags_to_keep:
                string = string.replace(tag,'~~~')
            else:
                string = string.replace(tag,"")
        else:
            break
    while True:
        white_space = re.search(r"(\s)\1{5,}",string)
        if white_space:
            white_space = white_space.group()
            string = string.replace(white_space,' ')
        else:
            break
    string = string.replace("~~~",replace_by)
    return string

def write_data(data):
    print(f"writing data to file {output_filename}")
    keys = data[0].keys()

    df_temp = [[prod[key] for key in keys] for prod in data]

    file = pandas.ExcelWriter(output_filename)
    df = pandas.DataFrame(df_temp, columns=keys)
    df.to_excel(file, index=False)
    file.save()
    print(f"{len(data)} rows written to {output_filename}")


def link_missed(link):
    open('missing_links.txt', 'a', encoding='utf-8').write(link)


def add_code(data):
    for ind, prod in enumerate(data):           
        prod['SKU'] = str(ind + 1)
        prod['Code'] = str(ind + 1) + "VC" #Change this to extra "C" if another batch NOT NUMBERS
        prod['Title'] = prod['Title'] + ' ' + prod['Code']

    return data

def get_color_list(soup):
    color_div_list = soup.find_all('div',{'class':'usf-facet'})[-1].find_all('button',{'class':'usf-label usf-btn'})[1:]
    color_list = [btn.text.strip().lower() for btn in color_div_list]
    return list(set(color_list))

def get_color(title,color_list):
    for color in color_list:
        if title.lower().__contains__(color):
            return color.capitalize()
    else:
        return 'NA'

def scrape_item_data(link_data):
    global product_list
    ind = link_data[1]
    cnt = link_data[2]
    link_data = link_data[0]

    link = link_data[0]
    brand = link_data[1]
    color = link_data[2]
    size = link_data[3]
    price = link_data[4]
    cat = link_data[5]
    product_name = link_data[6]

    if size[0] == " ":
        size = size[1:]

    soup = prepare_soup(link)
    print(f"({ind+1}/{cnt}) opening link {link}")
    if not soup:
        link_missed(link)
        print(f"unable to fetch link {link}")
        return False

    if float(price[1:]) < 10:
        listing_price = float(price[1:]) * 1.7
        listing_price = listing_price + 3

    if float(price[1:]) > 10 and float(price[1:]) < 20:
        listing_price = float(price[1:]) * 1.45
        listing_price = listing_price + 3

    if float(price[1:]) >= 20 and float(price[1:]) < 30:
        listing_price = float(price[1:]) * 1.27
        listing_price = listing_price + 3

    if float(price[1:]) >= 30 and float(price[1:]) < 40:
        listing_price = float(price[1:]) * 1.2
        listing_price = listing_price + 3

    if float(price[1:]) >= 40 and float(price[1:]) < 50:
        listing_price = float(price[1:]) * 1.17
        listing_price = listing_price + 3

    if float(price[1:]) >= 50 and float(price[1:]) < 60:
        listing_price = float(price[1:]) * 1.12
        listing_price = listing_price + 3
    if float(price[1:]) >= 60 and float(price[1:]) < 70:
        listing_price = float(price[1:]) * 1.1
        listing_price = listing_price + 3
    if float(price[1:]) >= 70:
        listing_price = float(price[1:]) * 1.08
        listing_price = listing_price + 3

    image_div = soup.find('div', {
                          'class': 'Product__SlideshowNav Product__SlideshowNav--thumbnails'}).find_all('a')
    image_link_list = ['http:' + a.attrs['href'] for a in image_div]
    image_links = " | ".join(image_link_list)

    description = remove_html_tags_keeping_one_tag(str(soup.find(id='prod-tab-desc')),['<br>','<br/>'],'<br>')

    product_list.append(
        {
            'SKU': '',
            'Code': '',
            'Item Cat': cat,
            'Title': product_name,
            'Uploaded': Uploaded,
            'Price': price,
            'Listing Price': listing_price,
            'Size': size,
            'Colour': color,
            'Brand': brand,
            'Description': description,
            'Image url': image_links,
            'item url': link
        }
    )


def scrape(link, item_cat):
    try:
        print(f"opening link {link}")
        #soup = prepare_soup(link)
        driver = get_selenium_driver()
        driver.get(link)
        driver.implicitly_wait(5)
        old_url = link
        print("Initiating page scrolling ... wait. this may take time")
        while True:
            driver.execute_script(
                'window.scrollTo(0,document.body.scrollHeight)')
            sleep(5)
            if old_url == driver.current_url:
                break
            old_url = driver.current_url
        sleep(10)

        soup = get_soup(driver.page_source)
        if not soup:
            link_missed(link)
            print(f"unable to fetch link {link}")
            return False

        div_list = soup.find_all('div', {'class': 'ProductItem'})
        color_list = get_color_list(soup)
        for div in div_list:
            a_tag = div.find('a')
            item_link = base_url + a_tag.attrs['href']
            brand = div.find(
                'p', {'class': 'ProductItem__Vendor Heading'}).text.strip()
            title = div.find(
                'h2', {'class': 'ProductItem__Title Heading'}).text.strip()
            size = title.split("-")[-1]
            color = get_color(title,color_list)
            price = div.find(
                'span', {'class': 'ProductItem__Price'}).text.strip().replace(",", '')

            yield (item_link, brand, color, size, price, item_cat, title)

    except Exception as e:
        print(e)
    finally:
        try:
            driver.quit()
        except:
            pass


def out_filename():
    time_now = str(datetime.now())
    for char in ['-', ':', ".", " "]:
        time_now = time_now.replace(char, '_')
    try:
        mkdir('output')
    except Exception:
        pass
    return "output/" + time_now + ".xlsx"


def scrap_item_datas_in_thread(link_list):
    POOL_SIZE = multiprocessing.cpu_count() * 2
    print(f"allotting {POOL_SIZE} threads for multiprocessing")
    cnt = len(link_list)
    with concurrent.futures.ThreadPoolExecutor(max_workers=POOL_SIZE) as executor:
        executor.map(scrape_item_data, [(link, ind, cnt)
                                        for ind, link in enumerate(link_list)])


if __name__ == "__main__":
    start = time()
    product_list = []
    sweat_shirt = [
        'https://vintageclub.uk/collections/mens-sweatshirts-and-hoodies', '155183']
    jackets = [
        'https://vintageclub.uk/collections/mens-jackets-and-coats', '185702']
    Uploaded = False
    base_url = 'https://vintageclub.uk/'
    #output_filename = r'cloth details.xlsx'
    output_filename = out_filename()

    link_list = []
    try:
        for link, item_cat in [sweat_shirt,jackets]:
            link_list += scrape(link, item_cat)

        link_count = len(link_list)
        print(f"{link_count} items found")

        print("Scrapping items data")

        scrap_item_datas_in_thread(link_list)
    except Exception as e:
        print(e)
    finally:
        write_data(add_code(product_list))

    end = time()  # Finishing Time
    time_spent = end - start  # Time taken by script

    print(
        "script ran for: %.2f minutes (%d seconds)"
        % (((time_spent) / 60), (time_spent))
    )

