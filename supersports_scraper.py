import requests
from bs4 import BeautifulSoup
import time
import json
import os

def scrapeSupersportsProducts(url, product_list):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15'
    }

    while True:
        try:
            print(f"Requesting URL: {url}")  # Debug print
            response = requests.get(url, headers=headers)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')
            print("Page content:", soup.prettify()[:1000])  # Print the first 1000 characters for inspection

            products = soup.find_all('div', class_='product-card')  # Check if this class is correct
            print(f"Found {len(products)} products")  # Debug print

            if not products:
                print("No products found on this page.")
                break
            
            for product in products:
                product_info = {}
                image_tag = product.find('img')
                if image_tag:
                    product_info['image_url'] = image_tag.get('data-src', '')
                
                name_tag = product.find('h3')
                if name_tag:
                    product_info['name'] = name_tag.text.strip()
                product_link = product.find('a', href=True)
                if product_link:
                    product_info['product_url'] = product_link['href']
                
                sku_tag = product.find('div', class_='sku')
                if sku_tag:
                    product_info['sku'] = sku_tag.text.strip()
                price_new_tag = product.find('span', class_='price-new')
                price_old_tag = product.find('span', class_='price-old')
                if price_new_tag:
                    product_info['sale_price'] = price_new_tag.text.strip()
                if price_old_tag:
                    product_info['drake_price'] = price_old_tag.text.strip()
                discount_tag = product.find('span', class_='label-discount')
                if discount_tag:
                    product_info['discount'] = discount_tag.text.strip()

                # Scrape product detail information
                try:
                    product_detail_response = requests.get(product_info['product_url'], headers=headers)
                    product_detail_response.raise_for_status()
                    product_detail_soup = BeautifulSoup(product_detail_response.content, 'html.parser')

                    size_select = product_detail_soup.find('select', id=lambda x: x and 'size' in x)
                    if size_select:
                        sizes = [option.text.strip() for option in size_select.find_all('option') if 'Select Size' not in option.text.strip()]
                        product_info['sizes'] = sizes

                    attribute_groups = product_detail_soup.find_all('div', class_='attribute-group')
                    for group in attribute_groups:
                        h3_tag = group.find('h3')
                        if h3_tag and 'Product Details' in h3_tag.text:
                            attributes = group.find('ul', class_='attribute-list')
                            if attributes:
                                for attribute in attributes.find_all('li'):
                                    label = attribute.find('label', class_='label')
                                    data = attribute.find('span', class_='data')
                                    if label and data:
                                        label_text = label.get_text(strip=True).replace(':', '')
                                        data_text = data.get_text(separator="\n", strip=True)
                                        if label_text and data_text:
                                            if label_text == "Gender":
                                                product_info['gender'] = data_text
                                            elif label_text == "Color":
                                                product_info['color'] = data_text
                                            elif label_text == "Upper Material":
                                                product_info['upper_material'] = data_text
                                            elif label_text == "Lining":
                                                product_info['lining'] = data_text
                                            elif label_text == "Sole":
                                                product_info['sole'] = data_text
                                            elif label_text == "Product Features":
                                                product_info['product_features'] = data_text
                except requests.RequestException as e:
                    print(f"Failed to retrieve product details: {e}")

                product_list.append(product_info)
                print(f"Product added: {product_info}")  # Debug print
                time.sleep(2)

            pagination = soup.find('ul', class_='pagination')
            if pagination:
                next_link = pagination.find('a', string='>')
                if next_link and next_link.get('href'):
                    url = next_link['href']
                else:
                    break
            else:
                break

        except requests.RequestException as e:
            print(f"Failed to retrieve page: {e}")
            break

def scrapAllRoutes():
    url_list = [
        "https://supersports.com.vn/collections/dep-quai-ngang?gioi_tinh=Nam",
        "https://supersports.com.vn/collections/dep-xo-ngon?gioi_tinh=Nam",
        "https://supersports.com.vn/collections/giay-bong-ro?gioi_tinh=Nam",
        "https://supersports.com.vn/collections/giay-chay-bo-nam",
        "https://supersports.com.vn/collections/giay-bong-da?gioi_tinh=Nam",
        "https://supersports.com.vn/collections/giay-di-bo?gioi_tinh=Nam",
        "https://supersports.com.vn/collections/giay-leo-nui?gioi_tinh=Nam",
        "https://supersports.com.vn/collections/giay-slip-on?gioi_tinh=Nam"
    ]
    
    product_list = []
    
    if os.path.exists('supersports.json'):
        with open('supersports.json', 'r', encoding='utf-8') as json_file:
            product_list = json.load(json_file)
    
    for url in url_list:
        scrapeSupersportsProducts(url, product_list)
        
    with open('supersports.json', 'w', encoding='utf-8') as json_file:
        json.dump(product_list, json_file, indent=4, ensure_ascii=False)
    
    print("Scraping completed. Data saved to 'supersports.json'.")

# Run the scraping function
scrapAllRoutes()
