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
        pageIndex = 1;
        try:
            print(f"Requesting URL: {url}")  # Debug print
            response = requests.get(url + '&page=' + str(pageIndex), headers=headers)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')
            print("Page content:", soup.prettify()[:1000])  # Print the first 1000 characters for inspection

            products = soup.find_all('div', class_='boost-pfs-filter-product-item-inner')  # Check if this class is correct
            print(f"Found {len(products)} products")  # Debug print

            if not products:
                print("No products found on this page.")
                break
            
            for product in products:
                product_info = {}
                image_tag = product.select('img[class^="boost-pfs-filter-product-item-main"]')
                if image_tag:
                    product_info['image_url'] = image_tag[0].get('data-img-flip-src', '')
                
                name_tag = product.select('[class="boost-pfs-filter-product-item-title"]')
                if name_tag:
                    product_info['name'] = name_tag[0].text.strip()
                product_link = product.find('a', class_='boost-pfs-filter-product-item-title', href=True)
                if product_link:
                    product_info['product_url'] = product_link['href']
                
                # sku_tag = product.find('div', class_='sku')
                # if sku_tag:
                #     product_info['sku'] = sku_tag.text.strip()
                price_new_tag = product.find('p', class_='boost-pfs-filter-product-item-price').find('span')
                price_old_tag = product.find('p', class_='boost-pfs-filter-product-item-price').find('s')
                if price_new_tag:
                    product_info['sale_price'] = price_new_tag.text.strip()
                if price_old_tag:
                    product_info['price'] = price_old_tag.text.strip()
                discount_tag = product.select('[class^="sale boost-pfs-filter-label boost-pfs"]')
                if discount_tag:
                    product_info['discount'] = discount_tag[0].text.strip()

                # Scrape product detail information
                try:
                    product_detail_response = requests.get('https://supersports.com.vn/' + product_info['product_url'], headers=headers)
                    product_detail_response.raise_for_status()
                    product_detail_soup = BeautifulSoup(product_detail_response.content, 'html.parser')

                    size_select = product_detail_soup.select('input[type="radio"]')
                    if size_select:
                        sizes = [option.get('value').strip() for option in size_select]
                        product_info['sizes'] = sizes

                    attribute_groups = product_detail_soup.find_all('table', class_='attr-flat-table')
                    for group in attribute_groups:
                        infos = group.select('tr')
                        for item in infos:
                            label = item.select('td')[0]
                            data = item.select('td')[1]
                            if label and data:
                                label_text = label.get_text(strip=True).replace(':', '')
                                data_text = data.get_text(separator="\n", strip=True)
                                if label_text and data_text:
                                    if "Chất liệu thân giày" in label_text:
                                        product_info['lining'] = data_text
                                    elif "Công nghệ" in label_text:
                                        product_info['product_features'] = data_text

                except requests.RequestException as e:
                    print(f"Failed to retrieve product details: {e}")

                product_list.append(product_info)
                print(f"Product added: {product_info}")  # Debug print
                time.sleep(2)

            pageIndex += 1

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
