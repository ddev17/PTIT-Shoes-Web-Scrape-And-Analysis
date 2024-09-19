import pickle
import urllib.parse
import requests
from bs4 import BeautifulSoup
import json
from pprint import pprint
import re

with open('product_link', 'rb') as f:
    product_links = pickle.load(f)

base_url = 'https://www.adidas.com.vn/'
headers = (
    {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15',
    }
)


def get_data(product_link):
    url = urllib.parse.urljoin(base_url, product_link)
    print(f'Crawling: {url}...')

    response: requests.Response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        scripts = soup.find_all('script')

        try:
            result_data = dict()
            for i in range(len(scripts)):
                if 'window.REACT_QUERY_DATA' in scripts[i].text and 'usps' in scripts[i].text:
                    index = scripts[i].text.find('{')
                    txt = scripts[i].text[index:]
                    data = json.loads(txt)
                    data = data['queries'][0]['state']['data']

                    price = data['pricing_information']['currentPrice']
                    gender = data['attribute_list']['gender']
                    usps = data['product_description']['usps']
                    usps = json.dumps(usps, ensure_ascii=False)
                    attribute_list = data['attribute_list']
                    attribute_list = json.dumps(
                        attribute_list, ensure_ascii=False)
                    variation_list = data['variation_list']
                    variation_list = json.dumps(variation_list)

                    result_data['price'] = price
                    result_data['gender'] = gender
                    result_data['usps'] = usps
                    result_data['attribute_list'] = attribute_list
                    result_data['variation_list'] = variation_list
                    break
            # pprint(scripts[0].text)
            data = json.loads(scripts[0].text)
            result_data['color'] = data['color']
            result_data['rating'] = data['aggregateRating']['ratingValue']
            result_data['description'] = data['description']
            result_data['name'] = data['name']
            result_data['material'] = data['material']

            pprint(result_data)
            return result_data
        except:
            return {}
    else:
        print("Status code 403")
        return {}

    return {}


datas = []
try:
    with open('data.pkl', 'rb') as f:
        datas = pickle.load(f)
except:
    pass

for i in range(len(datas), len(product_links)):
    data = get_data(product_links[i])

    while not bool(data):
        print("Error, try again...")
        data = get_data(product_links[i])

    datas.append(data)

    break
    with open('data.pkl', 'wb') as f:
        pickle.dump(datas, f)
