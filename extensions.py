import requests
import json
from config import available_currency


class APIException(Exception):
    pass


class GottenCurrency:
    @staticmethod
    def get_price(base, quote, amount):
        if not available_currency.get(base):
            raise APIException(f'Неправильное название валюты "{base}" или ее нет в списке!')
        elif not available_currency.get(quote):
            raise APIException(f'Неправильное название валюты "{quote}" или ее нет в списке!')
        elif base == quote:
            raise APIException("Одинаковые валюты!")
        if not amount.isdigit() or int(amount) <= 0:
            raise APIException("Количество первой валюты!")
        request_currency = requests.get(f'https://api.apilayer.com/fixer/convert?to={available_currency[quote]}\
&from={available_currency[base]}&amount={amount}', {"apikey": 'wabT2uTsxApcWjQdCN1ukNf1vGupRhUz'}).content
        return json.loads(request_currency)["result"]
