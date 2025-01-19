from pycbrf.toolbox import ExchangeRates
import datetime
from math import ceil
import requests
from config import COURSE_TOKEN
from bs4 import BeautifulSoup


def get_course_cny(n):
    current_date = str(datetime.date.today().isoformat())
    rates = ExchangeRates(current_date)  # задаем дату, за которую хотим получить данные
    result = rates['CNY']
    '''
        Внутри объекта result будут храниться следующие данные:
        ExchangeRate(
                    id='R01235',
                    name='Доллар США',
                    code='USD',
                    num='840',
                    value=Decimal('65.5287'),
                    par=Decimal('1'),
                    rate=Decimal('65.5287'))
        Можем обратиться к ним так:
        result.name # вернет Доллар США
        '''
    return int(ceil(n / result.value))


def get_exchange_rate():
    url = "https://api.exchangerate-api.com/v4/latest/RUB"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return data['rates']['CNY']  # Получаем курс юаня
    else:
        print("Ошибка при получении данных:", response.status_code)
        return None


def get_course_rub(n):
    exchange_rate = get_exchange_rate()
    if exchange_rate is not None:
        amount_cny = n * (exchange_rate + 2)
        return ceil(amount_cny)
    else:
        return None


if __name__ == "__main__":
    pass
