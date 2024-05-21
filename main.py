from environs import Env

from MarketAPI import Market, Shop


def main():
    env = Env()
    env.read_env()
    api_key = env.str('API_KEY')

    market = Market(api_key)
    shops = market.get_shops()
    for shop in shops.get('items'):
        shop = Shop(
            shop.get('id'),
            shop.get('organizationId'),
            shop.get('name'),
            shop.get('address'),
            shop.get('isPaid')
        )

    print(Shop.show_shops())


if __name__ == '__main__':
    main()
