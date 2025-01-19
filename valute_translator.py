from pycbrf.toolbox import ExchangeRates
import datetime
from math import ceil
import requests
from config import COURSE_TOKEN
from bs4 import BeautifulSoup

import requests


def get_exchange_rate():
    """
    Получает текущий курс обмена юаня к рублю.

    :return: Курс обмена юаня к рублю
    """
    url = "https://api.exchangerate-api.com/v4/latest/CNY"  # API для получения курса
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return data['rates']['RUB']  # Возвращаем курс рубля
    else:
        raise Exception("Ошибка при получении данных о курсе обмена.")


def get_course_rub(price_in_yuan):
    """
    Конвертирует цену товара из юаней в рубли.

    :param price_in_yuan: Цена товара в юанях
    :return: Цена товара в рублях
    """
    exchange_rate = get_exchange_rate()  # Получаем курс обмена
    price_in_ruble = price_in_yuan * exchange_rate
    return price_in_ruble


if __name__ == "__main__":
    pass
