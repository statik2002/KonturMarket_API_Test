from pprint import pprint
from environs import Env
import requests

env = Env()
env.read_env()

url = 'https://api.kontur.ru/market/v1/shops'

header = {
    'x-kontur-apikey': env('API_KEY')
}

response = requests.get(url, headers=header)
response.raise_for_status()

shops = response.json()

first_shop = shops['items'][0]

shop_id = first_shop['id']
shop_name = first_shop["name"]
shop_organizationId = first_shop["organizationId"]
shop_address = first_shop["address"]

leftovers_url = 'https://api.kontur.ru/market/v1/shops/{}/product-rests'.format(shop_id)
response = requests.get(leftovers_url, headers=header)
response.raise_for_status()

products = response.json()['items']

pprint(products[:20])
