import requests
from bs4 import BeautifulSoup
import csv

def scrape_product_listing(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    products = soup.find_all('div', {'data-component-type': 's-search-result'})

    results = []
    for product in products:
        product_url = 'https://www.amazon.in' + product.find('a', {'class': 'a-link-normal'})['href']
        product_name = product.find('span', {'class': 'a-size-medium'}).text.strip()
        product_price = product.find('span', {'class': 'a-offscreen'}).text.strip()
        rating = product.find('span', {'class': 'a-icon-alt'}).text.strip().split(' ')[0]
        num_reviews = product.find('span', {'class': 'a-size-base'}).text.strip()

        results.append({
            'Product URL': product_url,
            'Product Name': product_name,
            'Product Price': product_price,
            'Rating': rating,
            'Number of Reviews': num_reviews
        })

    return results

def scrape_product_details(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    description_elem = soup.find('div', {'id': 'productDescription'})
    description = description_elem.get_text(strip=True) if description_elem else ''

    asin_elem = soup.find('th', text='ASIN')
    asin = asin_elem.find_next('td').get_text(strip=True) if asin_elem else ''

    product_description_elem = soup.find('div', {'id': 'productDescription'})
    product_description = product_description_elem.get_text(strip=True) if product_description_elem else ''

    manufacturer_elem = soup.find('th', text='Manufacturer')
    manufacturer = manufacturer_elem.find_next('td').get_text(strip=True) if manufacturer_elem else ''

    return {
        'Description': description,
        'ASIN': asin,
        'Product Description': product_description,
        'Manufacturer': manufacturer
    }

base_url = 'https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_'
num_pages = 20
results = []

for page in range(1, num_pages + 1):
    url = base_url + str(page)
    results.extend(scrape_product_listing(url))

num_urls = 200
scraped_data = []

for i, product in enumerate(results[:num_urls], 1):
    print(f"Scraping product {i}/{num_urls}")
    product_url = product['Product URL']
    product_details = scrape_product_details(product_url)
    product.update(product_details)
    scraped_data.append(product)

keys = ['Product URL', 'Product Name', 'Product Price', 'Rating', 'Number of Reviews',
        'Description', 'ASIN', 'Product Description', 'Manufacturer']

filename = 'scraped_data.csv'
with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=keys)
    writer.writeheader()
    writer.writerows(scraped_data)

print(f"Scraped data saved to {filename}")
