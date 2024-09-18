import os
import requests
from bs4 import BeautifulSoup
import time
import json
import base64

# Function to convert image URL to Base64
def image_to_base64(image_url):
    try:
        response = requests.get(image_url)
        if response.status_code == 200:
            return base64.b64encode(response.content).decode('utf-8')
    except Exception as e:
        print(f"Error fetching image {image_url}: {e}")
    return None  # Return None if there's an error or the image cannot be fetched

# ////////////////////////////////////////////////////

# Function to scrape product details from a given URL
def scrapeNewBalanceProducts(url, product_list):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15'
    }

    while True:
        # Fetch the page
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            products = soup.find_all('div', class_='product-layout')

            # Break the loop if no products are found
            if not products:
                break
            
            for product in products:
                product_info = {}
                image_tag = product.find('img')
                if image_tag:
                    # Handle image fetch with error handling
                    try:
                        product_info['image_url'] = image_tag['src']
                    except Exception as e:
                        print(f"Error fetching image {image_tag['src']}: {e}")
                        product_info['image_url'] = None  # Skip the image if fetch fails
                        
                name_tag = product.find('h4')
                if name_tag:
                    product_info['name'] = name_tag.text.strip()
                product_link = product.find('a', href=True)
                if product_link:
                    product_info['product_url'] = product_link['href']
                                # SKU and pricing
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
                product_detail_response = requests.get(product_info['product_url'], headers=headers)
                if product_detail_response.status_code == 200:
                    product_detail_soup = BeautifulSoup(product_detail_response.content, 'html.parser')
                    attribute_groups = product_detail_soup.find_all('div', class_='attribute-group')
                    for group in attribute_groups:
                        h3_tag = group.find('h3')
                        if h3_tag and 'Đặc tính sản phẩm' in h3_tag.text:
                            attributes = group.find('ul', class_='attribute-list')
                            if attributes:
                                for attribute in attributes.find_all('li'):
                                    label = attribute.find('label', class_='label')
                                    data = attribute.find('span', class_='data')
                                    if label and data:
                                        label_text = label.get_text(strip=True).replace(':', '')
                                        data_text = data.get_text(separator="\n", strip=True)
                                        if label_text and data_text:
                                            if label_text == "Giới tính":
                                                product_info['gender'] = data_text
                                            elif label_text == "Màu sắc":
                                                product_info['color'] = data_text
                                            elif label_text == "Phần thân":
                                                product_info['upper_material'] = data_text
                                            elif label_text == "Lớp lót":
                                                product_info['lining'] = data_text
                                            elif label_text == "Đế giày":
                                                product_info['sole'] = data_text
                                            elif label_text == "Tính năng sản phẩm":
                                                product_info['product_features'] = data_text

                # Append the product information to the list
                product_list.append(product_info)

                # Pause to avoid overwhelming the server
                time.sleep(2)

            # Find and follow the pagination 'next' link (>)
            pagination = soup.find('ul', class_='pagination')
            if pagination:
                next_link = pagination.find('a', string='>')
                if next_link and next_link['href']:
                    url = next_link['href']  # Update the URL to the next page
                else:
                    break  # No more pages, exit the loop
            else:
                break  # No pagination found, exit the loop

        else:
            print(f"Failed to retrieve page with status code: {response.status_code}")
            break


# Function to scrape all routes and save to a single JSON file
def scrapAllRoutes():
    url_list = [
        "https://drake.vn/new-balance", 
        "https://drake.vn/converse", 
        "https://drake.vn/palladium", 
        "https://drake.vn/sneaker-buzz", 
        "https://drake.vn/ncaa", 
        "https://drake.vn/k-swiss", 
        "https://drake.vn/supra", 
        "https://drake.vn/accessoriesapparel",
        "https://drake.vn/vans"
    ]
    
    # Initialize an empty list to store all products
    product_list = []
    
    # Load existing data if the file exists
    if os.path.exists('drake.json'):
        with open('new_balance_products.json', 'r', encoding='utf-8') as json_file:
            product_list = json.load(json_file)

    # Loop through each URL and scrape products
    for url in url_list:
        scrapeNewBalanceProducts(url, product_list)
        
    # Save the combined data to a JSON file with utf-8 encoding
    with open('new_balance_products.json', 'w', encoding='utf-8') as json_file:
        json.dump(product_list, json_file, indent=4, ensure_ascii=False)
    
    print("Scraping completed. Data saved to 'new_balance_products.json'.")

# Run the scraping function
scrapAllRoutes()
