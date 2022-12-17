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

pprint(response.json())
