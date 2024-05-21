import requests


class Shop:
    shops = []

    def __init__(self, shop_id: str, organization_id: str, name: str, address: str, is_paid: bool) -> None:
        self.shop_id = shop_id
        self.organization_id = organization_id
        self.name = name
        self.address = address
        self.is_paid = is_paid
        Shop.shops.append(self)

    def __str__(self) -> str:
        return f'{self.shop_id}, {self.organization_id}, {self.name}, {self.address}, {self.is_paid}'

    @classmethod
    def show_shops(cls) -> str:
        shop_str = ''
        for shop in cls.shops:
            shop_str = shop_str + shop.__str__()
        return shop_str


class Market:

    def __init__(self, api_key: str) -> None:
        self._api_key = api_key

    def get_shops(self) -> dict:
        url = 'https://api.kontur.ru/market/v1/shops'

        header = {
            f'x-kontur-apikey': self._api_key
        }
        response = requests.get(url, headers=header)
        response.raise_for_status()

        return response.json()
