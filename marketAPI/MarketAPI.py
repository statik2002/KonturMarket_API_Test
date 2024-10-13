import requests


class Market:

    def __init__(self, api_key: str) -> None:
        self._api_key = api_key

    def get_shops(self) -> None:
        url = 'https://api.kontur.ru/market/v1/shops'

        header = {
            f'x-kontur-apikey': self._api_key
        }
        response = requests.get(url, headers=header)
        response.raise_for_status()

        for shop in response.json().get('items'):
            Shop(
                self._api_key,
                shop.get('id'),
                shop.get('organizationId'),
                shop.get('name'),
                shop.get('address'),
                shop.get('isPaid')
            )

        return

    def __str__(self) -> str:
        return f'{self._api_key}'


class Shop(Market):
    shops = []

    def __init__(self, api_key: str, shop_id: str, organization_id: str, name: str, address: str, is_paid: bool) -> None:
        super().__init__(api_key)
        self.shop_id = shop_id
        self.organization_id = organization_id
        self.name = name
        self.address = address
        self.is_paid = is_paid
        Shop.shops.append(self)

    def __str__(self) -> str:
        return f'{self.shop_id}, {self.organization_id}, {self.name}, {self.address}, {self.is_paid}'

    @classmethod
    def first(cls):
        return cls.shops[0]

    @classmethod
    def show_shops(cls) -> str:
        shop_str = ''
        for shop in cls.shops:
            shop_str = shop_str + shop.__str__()
        return shop_str

    def get_leftover(self) -> dict:
        url = f'https://api.kontur.ru/market/v1/shops/{self.shop_id}/product-rests'
        header = {
            f'x-kontur-apikey': self._api_key
        }
        response = requests.get(url, headers=header)
        response.raise_for_status()

        return response.json()

    def fetch_catalog(self) -> dict:
        url = f'https://api.kontur.ru/market/v1/shops/{self.shop_id}/product-groups'
        header = {
            f'x-kontur-apikey': self._api_key
        }
        response = requests.get(url, headers=header)
        response.raise_for_status()

        return response.json().get('items')


class Product(Market):
    products = []

    def __init__(self, api_key: str, shop_id: str, product_id: str, rest: float) -> None:
        super().__init__(api_key)
        self.shop_id = shop_id
        self.product_id = product_id
        self.rest = rest
        Product.products.append(self)

    def __str__(self) -> str:
        return f'{self.product_id}, {self.rest}, {self.shop_id}'

    def get_product_info(self) -> dict:
        url = f'https://api.kontur.ru/market/v1/shops/{self.shop_id}/products/{self.product_id}'
        header = {
            f'x-kontur-apikey': self._api_key
        }
        response = requests.get(url, headers=header)
        response.raise_for_status()

        return response.json()

