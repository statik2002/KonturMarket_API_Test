from environs import Env

from MarketAPI import Market, Shop, Product


def main():
    env = Env()
    env.read_env()
    api_key = env.str('API_KEY')

    market = Market(api_key)
    shops = market.get_shops()
    for shop in shops.get('items'):
        shop = Shop(
            api_key,
            shop.get('id'),
            shop.get('organizationId'),
            shop.get('name'),
            shop.get('address'),
            shop.get('isPaid')
        )

    print(Shop.show_shops())
    # print(market)
    leftovers = Shop.shops[0].get_leftover()
    #print(leftovers.get('currentDate'))
    for product in leftovers.get('items'):
        Product(api_key, Shop.shops[0].shop_id, product.get('productId'), product.get('rest'))

    #for product in Product.products:
    #    print(product)

    products_info = Product.products[0].get_product_info()
    print(products_info)



if __name__ == '__main__':
    main()
