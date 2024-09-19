import requests
from bs4 import BeautifulSoup
import json
import pprint
import pickle

def get_products_id(url: str, start: str) -> list[str]:
    url: str = f'{url}&start={start}'
    print(f'Crawling: {url}')
    headers = (
        {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15',
        }
    )

    response : requests.Response = requests.get(url, headers=headers)
    data = json.loads(response.text)

    ids = []
    for item in data['raw']['itemList']['items']:
        ids.append(item['link'])
    return ids

urls_list = [
    'https://www.adidas.com.vn/api/plp/content-engine?sitePath=vi&experiment=ATP-6974SWAvi&query=nu-giay',
    'https://www.adidas.com.vn/api/plp/content-engine?sitePath=vi&experiment=ATP-6974SWAvi&query=nam-giay',
]
ids_list = []

for url in urls_list:
    index = 0
    while True:
        ids = get_products_id(url, index)
        if len(ids) == 0:
            break
        ids_list.extend(ids)
        index += 48

ids_list = list(dict.fromkeys(ids_list))
with open('product_link', 'wb') as fp:
    pickle.dump(ids_list, fp)


