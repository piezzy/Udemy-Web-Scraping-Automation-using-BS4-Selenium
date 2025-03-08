from datetime import datetime
import requests
import csv
import bs4
import os

filepath = os.path.abspath("amazon_products_urls.csv")

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36 Edg/133.0.0.0'
REQUEST_HEADERS = {
    'User-Agent': USER_AGENT,
    'Accept-Language': 'en-US,en;q=0.5',
}

def get_page_html(url):
    res = requests.get(url=url,headers=REQUEST_HEADERS)
    return res.content

def get_product_price(soup):
    main_price_span = soup.find('span', attrs={
        "class": "a-price aok-align-center reinventPricePriceToPayMargin priceToPay"
    })
    price_span = main_price_span.find_all('span')
    for span in price_span:
        price = span.text.strip().replace('$', '').replace(',', '')
        try:
            return float(price)
        except ValueError:
            print("cannot be parsed")
            
def get_product_title(soup):
    prouduct_title = soup.find('span', id="productTitle")
    return prouduct_title.text.strip()

def get_product_rating(soup):
    product_rating = soup.find('span', attrs={"id": "averageCustomerReviews"})
    if not product_rating:
        print("Product rating not found")
        return None
    
    product_rating_section = product_rating.find('i', class_="a-icon-star")
    if not product_rating_section:
        print("Rating section not found")
        return None
    
    product_rating_span = product_rating_section.find('span')
    if not product_rating_span:
        print("Rating span not found")
        return None

    try:
        rating = product_rating_span.text.strip().split()
        print(rating)
        return float(rating[0]) 
    except ValueError:
        print("Rating cannot be parsed")
        return None

def get_product_details(soup):
    details = {}
    details_section = soup.find('div', id="prodDetails")
    data_table = details_section.find_all('table', class_='prodDetTable')
    for table in data_table:
        table_rows = table.find_all('tr')
        for row in table_rows:
            key = row.find('th').text.strip()
            value = row.find('td').text.strip().replace('\u200e', '')
            details[key] = value
    return details
                                                                
                                                                 
def extract_product_info(url):
    product_info = {}
    print("Extracting product info from: ", url)
    html = get_page_html(url)
    soup = bs4.BeautifulSoup(html, 'lxml')
    product_info['price'] = get_product_price(soup)
    product_info['title'] = get_product_title(soup)
    product_info['rating'] = get_product_rating(soup)
    product_info.update(get_product_details(soup))
    print(product_info)
    
    
if __name__ == "__main__":
    with open(filepath, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            url = row[0]
            extract_product_info(url)