import requests

def get_product(shop_id, product_id, api_key):
    url = 'https://api.kontur.ru/market/v1/shops/{}/products/{}'.format(shop_id, product_id)

    header = {
    'x-kontur-apikey': api_key
    }

    response = requests.get(url, headers=header)
    response.raise_for_status()

    return response.json()