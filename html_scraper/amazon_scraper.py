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
    
def extract_product_info(url):
    product_info = {}
    print("Extracting product info from: ", url)
    html = get_page_html(url)
    soup = bs4.BeautifulSoup(html, 'lxml')
    product_info['price'] = get_page_html(url)

if __name__ == "__main__":
    with open(filepath, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            url = row[0]
            print(extract_product_info(url))