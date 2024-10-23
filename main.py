from pprint import pprint

from environs import Env
from MarketAPI import Market, Shop, Product


def main():
    env = Env()
    env.read_env()
    api_key = env.str('API_KEY')

    # Созадаём экземпляр класса Маркет API
    market = Market(api_key)

    # Получаем список магазинов
    market.get_shops()

    first_shop = market.get_first_shop()
    print(first_shop.__dict__)
    #print(first_shop.__dict__)
    first_shop.fetch_catalog(api_key)

    first_shop.get_products(api_key)

    first_shop.get_rest(api_key)

    # for product in first_shop.get_positive_rest():
    #    print(product)

    cheques = first_shop.get_cheque_at_period(api_key, '2024-10-23', '2024-10-23')

    for cheque in cheques:
        print(cheque)


if __name__ == '__main__':
    main()
