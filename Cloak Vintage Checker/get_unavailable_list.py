from os import system

from numpy import fabs


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
        return BeautifulSoup(html.text,"html.parser")
    else:
        return False

def read_data():
    data = pandas.read_excel(input_file)
    return data

def product_available(link):
    soup = prepare_soup(link)
    if not soup:
        return False
    if soup.find_all('div',{'class':'product__price'})[0].text.strip().lower().__contains__('sold out'):
        return False
    return True


def get_unavailable_items_code():
    data = read_data()
    unavailable_list = []
    for ind in data.index:
        code = data['Code'][ind]
        link = data['item url'][ind]
        print(1)
        if not product_available(link):
            unavailable_list.append(code)
    return unavailable_list," ".join(unavailable_list)


if __name__ == "__main__":
    input_file = r"C:\Users\jackk\Desktop\GITHUB\EbayScraper\cloth data scraper Dev\cloth details.xlsx"

    out_list,out_string = get_unavailable_items_code()
    print(out_list)
    print(out_string)
    