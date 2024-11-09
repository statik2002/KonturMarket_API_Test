import requests
from datetime import datetime


UNIT = {
    'Piece': 'штука',
    'Package': 'упаковка',
    'Set': 'комплект',
    'Pair': 'пара',
    'Kit': 'набор',
    'Tonne': 'тонна',
    'Kilogram': 'килограмм',
    'Gram': 'грамм',
    'Milligram': 'миллиграмм',
    'CubicMeter': 'кубический метр',
    'Liter': 'литр',
    'Milliliter': 'миллилитр',
    'RunningMeter': 'погонный метр',
    'Kilometer': 'километр',
    'Meter': 'метр',
    'Centimeter': 'сантиметр',
    'Millimeter': 'миллиметр',
    'SquareMeter': 'квадратный метр',
    'SquareCentimeter': 'квадратный сантиметр',
    'Month': 'месяц',
    'Week': 'неделя',
    'Day': 'день',
    'Hour': 'час',
    'Minute': 'минута',
    'KilowattHour': 'киловатт-час',
    'Gigacalorie': 'гигакалория',
    'MegawattHour': 'мегаватт-час',
}


class Market:

    __shops = []
    __api_key = ''

    @property
    def api_key(self) -> str:
        if not hasattr(self, '__api_key'):
            raise Exception('Property api_key not defined!')

        return str(self.__api_key)

    @api_key.setter
    def api_key(self, key):
        if not key:
            raise Exception('API key is empty')
        self.__api_key = key

    def get_shops(self) -> None:
        """
        Get all shops and save class property __shops
        :return: None
        """
        if not self.__class__.api_key:
            raise Exception('API Key is empty')

        url = 'https://api.kontur.ru/market/v1/shops'

        header = {
            f'x-kontur-apikey': self.__class__.api_key
        }
        response = requests.get(url, headers=header)
        response.raise_for_status()

        for shop in response.json().get('items'):
            self.__shops.append(
                Shop(
                    shop.get('id'),
                    shop.get('organizationId'),
                    shop.get('name'),
                    shop.get('address'),
                    shop.get('isPaid')
                )
            )

    def get_all_shops(self) -> list:
        """
        Return list of shops objects
        :return: List[Shop]
        """
        return self.__shops

    def get_shop(self, index: int) -> 'Shop':
        """
        Return Shop object from __shops by index
        :param index: list index at __shops list
        :return: Shop object
        """
        if not index.is_integer() or (0 > index > len(self.__shops) - 1):
            raise IndexError
        return self.__shops[index]

    def get_first_shop(self) -> 'Shop':
        """
        Return Shop object with index 0
        :return: Shop object
        """
        return self.__shops[0]


class Shop(Market):

    catalog = []
    products = []

    def __init__(self, shop_id: str, organization_id: str, name: str, address: str, is_paid: bool) -> None:
        self.shop_id = shop_id
        self.organization_id = organization_id
        self.name = name
        self.address = address
        self.is_paid = is_paid

    def __str__(self) -> str:
        return f'{self.shop_id}, {self.organization_id}, {self.name}, {self.address}, {self.is_paid}'

    def fetch_catalog(self) -> None:
        """
        Fetch shop catalog and save in self.catalog list
        :return:
        """
        url = f'https://api.kontur.ru/market/v1/shops/{self.shop_id}/product-groups'
        header = {
            f'x-kontur-apikey': self.__class__.api_key
        }
        response = requests.get(url, headers=header)
        response.raise_for_status()

        for cat in response.json().get('items'):
            self.catalog.append(
                Catalog(
                    cat.get('id'),
                    cat.get('parentId'),
                    cat.get('name')
                )
            )

    def get_products(self) -> None:
        """
        Fetch all products and save in self.products list
        :return:
        """
        url = f'https://api.kontur.ru/market/v1/shops/{self.shop_id}/products'
        header = {
            f'x-kontur-apikey': self.__class__.api_key
        }
        response = requests.get(url, headers=header)
        response.raise_for_status()

        for product in response.json().get('items'):
            self.products.append(
                Product(
                    product.get('id'),
                    product.get('shopId'),
                    product.get('name'),
                    product.get('groupId'),
                    UNIT[product.get('unit')],
                )
            )

    def get_product_by_id(self, product_id: str) -> dict:
        url = f'https://api.kontur.ru/market/v1/shops/{self.shop_id}/products/{product_id}'
        header = {
            f'x-kontur-apikey': self.__class__.api_key
        }
        response = requests.get(url, headers=header)
        response.raise_for_status()

        return response.json()

    def get_rest(self) -> None:
        """
        Fetch rest and save at Product.rest in products list
        :return: None
        """
        url = f'https://api.kontur.ru/market/v1/shops/{self.shop_id}/product-rests'
        header = {
            f'x-kontur-apikey': self.__class__.api_key
        }
        response = requests.get(url, headers=header)
        response.raise_for_status()

        fetched_products = response.json().get('items')

        for product in fetched_products:
            shop_product_index = next((index for (index, pr) in enumerate(self.products) if pr.id == product.get('productId')), None)
            if shop_product_index:
                self.products[shop_product_index].rest = float(product.get('rest'))

    def get_positive_rest(self) -> list['Product']:
        """
        Return list of Product objects with rest greater zero
        :return: List of Product objects
        """
        return list(filter(lambda product: product.rest > 0, self.products))

    def get_cheque_at_period(self, date_from: str, date_to: str) -> list:
        """
        Fetch all cheques at period
        :param date_from: start date
        :param date_to: end date
        :return: list of cheques
        """
        url = f'https://api.kontur.ru/market/v1/shops/{self.shop_id}/cheques'
        header = {
            f'x-kontur-apikey': self.__class__.api_key
        }
        params = {
            'dateFrom': date_from,
            'dateTo': date_to
        }
        response = requests.get(url, headers=header, params=params)
        response.raise_for_status()

        cheques = []

        # print(response.json().get('items'))

        for cheque in response.json().get('items'):
            lines = []
            for line in cheque.get('lines'):
                lines.append(
                    ReceiptLine(
                        product_id=line.get('productId'),
                        version_id=line.get('versionId'),
                        product_code=line.get('productCode'),
                        cheque_line_type=line.get('chequeLineType'),
                        sell_price_per_unit=float(line.get('sellPricePerUnit').replace(',', '.')),
                        count=float(line.get('count')),
                        tax_system=line.get('taxSystem'),
                        total_vat_value=line.get('totalVatValue'),
                        vat_rate=line.get('vatRate'),
                        discount_total_sum=float(line.get('discountTotalSum')),
                        point_discount_sum=line.get('pointsDiscountSum'),
                        calc_mode=line.get('calculationMode')
                    )
                )

            payments = []
            for payment in cheque.get('payments'):
                payments.append(
                    Payment(
                        payment.get('type'),
                        float(payment.get('value').replace(',', '.'))
                    )
                )

            cheques.append(
                Receipt(
                    cheque.get('id'),
                    cheque.get('shopID'),
                    cheque.get('number'),
                    cheque.get('cashboxId'),
                    cheque.get('cashRegisterId'),
                    cheque.get('openTime'),
                    cheque.get('closeTime'),
                    cheque.get('isRefund'),
                    cheque.get('totalPrice'),
                    cheque.get('priceCorrection'),
                    lines,
                    payments
                )
            )

        return cheques


class Catalog:
    def __init__(self, id: str, parent_id: str, name: str) -> None:
        self.id = id
        self.parent_id = parent_id
        self.name = name

    def __str__(self) -> str:
        return f'{self.id}, {self.parent_id}, {self.name}'


class Product:

    def __init__(self, id: str, shop_id: str, name: str, group_id: str, unit: str, rest: float = 0.0) -> None:
        self.id = id
        self.shop_id = shop_id
        self.name = name
        self.group_id = group_id
        self.unit = unit
        self.rest = rest

    def __str__(self) -> str:
        return f'{self.id}, {self.name}, {self.group_id}, {self.rest}, {self.unit}'


class Payment:
    def __init__(self, payment_type: str, value: float):
        self.payment_type = payment_type
        self.value = value

    def __str__(self):
        return f'Тип оплаты: {self.payment_type} - Сумма: {self.value} Руб.'


class Receipt:

    def __init__(self, id: str, shop_id: str, number: str, cashbox_id: str, cash_register_id: str,
                 open_time: datetime, close_time: datetime, is_refund: bool, total_price: float,
                 price_correction: float, lines: list, payment_type: list) -> None:
        self.id = id
        self.shop_id = shop_id
        self.number = number
        self.cashbox_id = cashbox_id
        self.cash_register_id = cash_register_id
        self.open_time = open_time
        self.close_time = close_time
        self.is_refund = is_refund
        self.total_price = total_price
        self.price_correction = price_correction
        self.lines = lines
        self.payment = payment_type

    def __str__(self) -> str:
        return f'{self.number}, {self.open_time}, {self.close_time}, Refund: {self.is_refund}, {self.total_price}, pr_cor: {self.price_correction}'

    def print_receipt(self):
        if self.is_refund:
            operation = 'Возврат'
        else:
            operation = 'Продажа'
        first_line = f'#{self.number} {self.open_time}-{self.close_time} {operation} на сумму: {self.total_price} Руб.'
        second_line = ''
        for payment in self.payment:
            second_line += f'Тип оплаты: {payment.payment_type} - Сумма: {payment.value} Руб.'

        return first_line + second_line


class ReceiptLine:
    def __init__(self, product_id: str, version_id: str, product_code: str, cheque_line_type: str,
                 sell_price_per_unit: float, count: float, tax_system: str, total_vat_value: float, vat_rate: str,
                 discount_total_sum: float, point_discount_sum: float,
                 calc_mode: str) -> None:
        self.product_id = product_id
        self.version_id = version_id
        self.product_code = product_code
        self.cheque_line_type = cheque_line_type
        self.sell_price_per_unit = sell_price_per_unit
        self.count = count
        self.tax_system = tax_system
        self.total_vat_value = total_vat_value
        self.vat_rate = vat_rate
        self.discount_total_sum = discount_total_sum
        self.point_discount_sum = point_discount_sum
        self.calc_mode = calc_mode

    def __str__(self):
        return f'Product Id: {self.product_id}, Code: {self.product_code}, price: {self.sell_price_per_unit} x Count: {self.count} - Discount: {self.discount_total_sum} = {self.sell_price_per_unit * self.count - self.discount_total_sum}'

