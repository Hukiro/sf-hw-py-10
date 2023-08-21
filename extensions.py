import requests
import json
from config import keys


class APIException(Exception):
    pass


class Convertor:
    @staticmethod
    def get_price(values):
        if len(values) != 3:
            raise APIException('Формат команды не верен.\nПример правильного запроса: /example')

        quote, base, amount = values

        if quote == base:
            raise APIException(f'Введена одинаковая валюта "{quote}".')

        try:
            fsym = keys[quote]
        except KeyError:
            raise APIException(f'Валюта "{quote}" не может быть обработана.\nПеречень доступных валют: /values')

        try:
            tsyms = keys[base]
        except KeyError:
            raise APIException(f'Валюта "{base}" не может быть обработана.\nПеречень доступных валют: /values')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Количество "{amount}" не может быть обработано.\nПример правильного запроса: /example')

        if quote == 'евро':
            ending_q = ''
        elif quote == 'рубль':
            if float(amount) == int(amount):
                amount = int(amount)
                if amount % 10 == 1 and amount % 100 != 11:
                    quote = 'рубля'
                    ending_q = ''
                else:
                    quote = 'рублей'
                    ending_q = ''
            else:
                quote = 'рубля'
                ending_q = ''
        else:
            if float(amount) == int(amount):
                amount = int(amount)
                if amount % 10 == 1 and amount % 100 != 11:
                    ending_q = 'a'
                else:
                    ending_q = 'ов'
            else:
                ending_q = 'a'

        if base == 'евро':
            ending_b = ''
        elif base == 'рубль':
            base = 'рублях'
            ending_b = ''
        else:
            ending_b = 'ах'

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={fsym}&tsyms={tsyms}')
        result = float(json.loads(r.content)[tsyms]) * float(amount)
        if result > 1:
            result = round(result, 3)
        text = f'цена {amount} {quote}{ending_q} в {base}{ending_b} - {result}'
        return text
