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

    # Выводим первый магазин
    first_shop = Shop.first()
    print(first_shop)
    # выводим каталог первого магазина
    pprint(first_shop.fetch_catalog())

    #leftovers = Shop.shops[0].get_leftover()
    #print(leftovers.get('currentDate'))
    #for product in leftovers.get('items'):
    #    Product(api_key, Shop.shops[0].shop_id, product.get('productId'), product.get('rest'))

    #for product in Product.products:
    #    print(product)

    #products_info = Product.products[0].get_product_info()
    #print(products_info)



if __name__ == '__main__':
    main()
