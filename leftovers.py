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

#pprint(first_shop)

print(f'id магазина = {first_shop["id"]}')
print(f'Название = {first_shop["name"]}')
print(f'Id организации = {first_shop["organizationId"]}')
print(f'Адрес организаци = {first_shop["address"]}')
