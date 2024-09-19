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

        for i in range(len(scripts)):
            if 'window.REACT_QUERY_DATA' in scripts[i].text and 'usps' in scripts[i].text:
                index = scripts[i].text.find('{')
                txt = scripts[i].text[index:]
                data = json.loads(txt)
                data = data['queries'][0]['state']['data']

                price = data['pricing_information']['currentPrice']
                gender = data['attribute_list']['gender']
                desc = data['product_description']['usps']
                desc = json.dumps(desc)

                return {'price': price, 'gender': gender, 'desc': desc}
    else:
        print("Status code 403")
        return {}

    return {}


datas = []
try:
    with open('data', 'rb') as f:
        datas = pickle.load(f)
except:
    pass

for i in range(len(datas), len(product_links)):
    datas.append(get_data(product_links[i]))

    with open('data', 'wb') as f:
        pickle.dump(datas, f)
