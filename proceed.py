from pprint import pprint
from environs import Env
import requests

env = Env()
env.read_env()

api_key = env('API_KEY')

url = 'https://api.kontur.ru/market/v1/shops'

header = {
    'x-kontur-apikey': api_key
}

response = requests.get(url, headers=header)
response.raise_for_status()

shops = response.json()

first_shop = shops['items'][0]

shop_id = first_shop['id']
shop_name = first_shop["name"]
shop_organizationId = first_shop["organizationId"]
shop_address = first_shop["address"]


cheques_url = 'https://api.kontur.ru/market/v1/shops/{}/cheques'.format(shop_id)

response = requests.get(cheques_url, headers=header)
response.raise_for_status()

proceed = response.json()['items']

for check in proceed:
    print(check['totalPrice'])

