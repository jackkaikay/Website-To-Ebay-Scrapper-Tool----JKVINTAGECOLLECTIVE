from os import system
import concurrent.futures
import multiprocessing

try:
    import pandas
    import requests
    from bs4 import BeautifulSoup
except ModuleNotFoundError:
    system("pip install -r requirements.txt")
    import pandas
    import requests
    from bs4 import BeautifulSoup


def prepare_soup(link):
    html = requests.get(link)
    if html.status_code == 200:
        return BeautifulSoup(html.text, "html.parser")
    else:
        return False


def write_data(data):
    print(f"writing data to file {output_filename}")
    keys = data[0].keys()

    df_temp = [[prod[key] for key in keys] for prod in data]

    file = pandas.ExcelWriter(output_filename)
    df = pandas.DataFrame(df_temp, columns=keys)
    df.to_excel(file, index=False)
    file.save()
    print(f"{len(data)} rows written to {output_filename}")


def get_brand_list(soup):
    selector = soup.find(id='Filterbrand').find_all('option')
    brand_list = []
    for option in selector:
        brand_list.append(option.text.strip())
    brand_list.remove('Brand')
    return brand_list


def get_color_list(soup):
    selector = soup.find(id='Filtercolour').find_all('option')
    color_list = []
    for option in selector:
        color_list.append(option.text.strip())
    color_list.remove('Colour')
    return color_list


def link_missed(link):
    open('missing_links.txt', 'a', encoding='utf-8').write(link)


def add_code(data):
    for ind, prod in enumerate(data):
        prod['Code'] = str(ind + 1) + "CLOAK-W"
        prod['Title'] = prod['Title'] + ' ' + prod['Code']

    return data


def scrape_item_data(link_data):
    global product_list

    def selector(item_list, name):
        for item in item_list:
            if name.__contains__(item):
                return item
        else:
            return False

    link = link_data[0]
    brand_list = link_data[1]
    color_list = link_data[2]
    cat = link_data[3]
    soup = prepare_soup(link)
    print(f"opening link {link}")
    if not soup:
        link_missed(link)
        print(f"unable to fetch link {link}")
        return False
    product_name = soup.find_all('h1', {'class': 'product-single__title'})[0].text.strip()
    brand = selector(brand_list, product_name)
    if not brand:
        brand = 'Unbranded'
    color = selector(color_list, product_name)
    if not color:
        color = product_name.split()[-2]
    price = soup.find_all('span', {'class': 'money'})[0].text.strip()
    if float(price[1:]) > 50:
        listing_price = float(price[1:]) * 1.45
    else:
        listing_price = float(price[1:]) * 1.7

    try:
        size = soup.find(id='SingleOptionSelector-0').option.attrs['value']
    except Exception:
        size = 'N/A'
    image_ul = soup.find_all('ul', {'class': 'product-single__thumbnails'})[0].findAll('li')
    image_link_list = ['http:' + li.a.attrs['href'] for li in image_ul]
    image_links = " | ".join(image_link_list)

    text_to_remove = 'Please check measurements and product description carefully.\n\xa0\nVintage & Sustainable Clothing'
    description = ((soup.find_all('div', {'class': 'product-single__description'})[0].text.strip().replace(
        text_to_remove, "")).replace('\xa0', '<br>')).replace('Description', "")
    product_list.append(
        {
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


def scrape(link):
    try:
        print(f"opening link {link}")
        soup = prepare_soup(link)
        if not soup:
            link_missed(link)
            print(f"unable to fetch link {link}")
            return False
        brand_list = get_brand_list(soup)
        color_list = get_color_list(soup)
        page_count = soup.find('li', {'class': 'pagination__text'}).text.strip().split()[-1]
        while True:
            collection_div = soup.find(id='Collection')
            li_list = collection_div.find_all('li')
            for li in li_list:
                if 'class' in li.attrs:
                    if 'grid__item--collection-template' in li.attrs['class']:
                        item_link = base_url + li.a.attrs['href']
                        yield (item_link, brand_list, color_list, item_cat)
            try:
                if link.partition('page=')[2] == page_count:
                    print("end of page")
                    break
                link = base_url + soup.find_all('ul', {'class': 'pagination'})[0].findAll('li')[2].find('a').attrs[
                    'href']
                print(f"opening link {link}")
                soup = prepare_soup(link)
            except Exception as e:
                print(e)
                break
    except Exception as e:
        print(e)


def scrap_item_datas_in_thread(link_list):
    POOL_SIZE = multiprocessing.cpu_count() * 2
    print(f"allotting {POOL_SIZE} threads for multiprocessing")
    with concurrent.futures.ThreadPoolExecutor(max_workers=POOL_SIZE) as executor:
        executor.map(scrape_item_data, [link for link in link_list])


if __name__ == "__main__":
    product_list = []
    links = ['https://www.cloakvintage.com/collections/sweaters/Ladies',
             'https://www.cloakvintage.com/collections/jackets-coats/Ladies']

    item_cat_list = {
        'sweaters': '155226',
        'jackets-coats': '185079'
    }
    Uploaded = False
    base_url = 'https://www.cloakvintage.com/'
    output_filename = r'Cloak Scrape - Mens.xlsx'

    link_list = []

    try:
        for link in links[::-1]:
            for item, cat in item_cat_list.items():
                if link.__contains__(item):
                    item_cat = cat
                    break
            print(f"""
            Base URL : {base_url}
            selected Cat : {item_cat}
            """)
            link_list += list(scrape(link))

        link_count = len(link_list)
        print(f"{link_count} items found")

        print("Scrapping items data")

        scrap_item_datas_in_thread(link_list)
    except Exception as e:
        print(e)
    finally:
        write_data(add_code(product_list))


