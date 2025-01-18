from pycbrf.toolbox import ExchangeRates
import datetime


def get_course():
    current_date = str(datetime.date.today().isoformat())
    rates = ExchangeRates(current_date)  # задаем дату, за которую хотим получить данные
    result = rates['CNY']
    print(result.value)
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

if __name__ == "__main__":
    get_course()
