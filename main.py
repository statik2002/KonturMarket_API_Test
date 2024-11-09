from pprint import pprint

from environs import Env
from MarketAPI import Market, Shop, Product


def main():
    env = Env()
    env.read_env()
    api_key = env.str('API_KEY')

    # Создаём экземпляр класса Маркет API
    market = Market()

    # Создаем свойство класса с ключом
    Market.api_key = api_key

    # Получаем список магазинов
    market.get_shops()

    # берем первый магазин
    first_shop = market.get_first_shop()

    # подгружаем каталог у выбранного магазина
    #first_shop.fetch_catalog()
    #for catalog in first_shop.catalog:
    #    print(catalog)

    # Подгружаем все товары
    #first_shop.get_products()

    # Подгружаем все остатки
    #first_shop.get_rest()

    #for product in first_shop.get_positive_rest():
    #    print(product)

    cheques = first_shop.get_cheque_at_period('2024-11-09', '2024-11-09')

    for cheque in cheques:
        print(cheque.print_receipt())
        for line in cheque.lines:
            product = first_shop.get_product_by_id(line.product_id)
            print(
                f'{product.get("name")}, {line.sell_price_per_unit} Руб. x {line.count} - {line.discount_total_sum} Руб = {line.sell_price_per_unit * line.count - line.discount_total_sum} Руб'
            )


if __name__ == '__main__':
    main()
