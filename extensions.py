import requests
import json
from config import available_currency, API_KEY


class APIException(Exception):
    pass


class GottenCurrency:
    @staticmethod
    def get_price(base, quote, amount):
        amount = amount.replace(',', '.')
        if not available_currency.get(base):
            raise APIException(f'Неправильное название валюты "{base}" или ее нет в списке!')
        elif not available_currency.get(quote):
            raise APIException(f'Неправильное название валюты "{quote}" или ее нет в списке!')
        elif base == quote:
            raise APIException("Одинаковые валюты!")
        try:
            if amount.isdigit():
                amount = int(amount)
            else:
                amount = float(amount)
            if amount <= 0:
                raise APIException("Количество первой валюты!")
        except Exception:
            raise APIException("Количество первой валюты!")
        request_currency = requests.get(f'https://api.apilayer.com/fixer/convert?to={available_currency[quote][0]}\
&from={available_currency[base][0]}&amount={amount}', API_KEY).content
        result_conversion = json.loads(request_currency)["result"]
        result = round(float(result_conversion), 2)
        if amount < 1:
            from_ = available_currency[base][1]
        elif amount > 1:
            from_ = available_currency[base][2]
        else:
            from_ = base
        if result < 1:
            to_ = available_currency[quote][1]
        elif result > 1:
            to_ = available_currency[quote][2]
        else:
            to_ = quote
        return result, from_, to_, amount

