import requests


def get_product(shop_id, product_id, api_key):
    url = 'https://api.kontur.ru/market/v1/shops/{}/products/{}'.format(shop_id, product_id)

    header = {
    'x-kontur-apikey': api_key
    }

    response = requests.get(url, headers=header)
    response.raise_for_status()

    return response.json()


def get_shops(api_key):
    url = 'https://api.kontur.ru/market/v1/shops'

    header = {
        'x-kontur-apikey': api_key
    }

    response = requests.get(url, headers=header)
    response.raise_for_status()

    return response.json()['items']


def get_today_proceed(api_key, shop_id):
    header = {
        'x-kontur-apikey': api_key
    }

    proceed_url = 'https://api.kontur.ru/market/v1/shops/{}/cheques'.format(shop_id)

    response = requests.get(proceed_url, headers=header)
    response.raise_for_status()

    return response.json()['items']

