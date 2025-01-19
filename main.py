import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from config import TOKEN
import asyncio
from get_yani import get_course_cny, get_course_rub

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher()


class Uyan(StatesGroup):
    calculate_price = State()


class Ruble(StatesGroup):
    calculate_price = State()


KEYBOARD_START = [
    [types.KeyboardButton(text="ОФОРМИТЬ ЗАКАЗ")],
    [types.KeyboardButton(text="ПЕРЕВЕСТИ ЮАНИ В РУБЛИ")],
    [types.KeyboardButton(text="ПЕРЕВЕСТИ РУБЛИ В ЮАНИ")],
    [types.KeyboardButton(text="ПОМОЩЬ")]
]


@dp.message(Command('start'))
async def start_message(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=KEYBOARD_START,
        resize_keyboard=True,
        input_field_placeholder="Нажмите на необходимую кнопку"
    )
    await message.answer('Добро пожаловать! Данный тг бот поможет вам оформить заказ с Poizon. Нажмите на '
                         'одну из кнопок ниже для продолжения работы:', reply_markup=keyboard)


@dp.message(F.text.lower() == "помощь")
async def help_message(message: types.Message):
    await message.answer('Здесь будет размещена помощь. Чтобы вернуться назад нажмите /start')


@dp.message(F.text.lower() == "перевести юани в рубли")
async def calculate_price_start(message: types.Message, state: FSMContext):
    await message.answer('Введите цену товара в рублях, я переведу Вам в юани (чтобы начать сначала введите /start)')
    await state.set_state(Uyan.calculate_price)


@dp.message(Uyan.calculate_price)
async def calculate_price(message: types.Message, state: FSMContext):
    try:
        price = int(message.text)
        print(price)
        new_price = get_course_cny(price)
        print(new_price)
        await message.answer(f"{price} RUB = {new_price} CNY")
        await message.answer(f"Нажмите /start, чтобы вернуться обратно")
        await state.clear()  # Очистить состояние после обработки
    except ValueError:
        await message.answer('Возникла ошибка, вероятно вы неправильно ввели данные. Вернитесь назад, нажав /start')


@dp.message(F.text.lower() == "перевести рубли в юани")
async def calculate_price_start(message: types.Message, state: FSMContext):
    await message.answer('Введите цену товара в рублях, я переведу Вам в юани (чтобы начать сначала введите /start)')
    await state.set_state(Ruble.calculate_price)


@dp.message(Ruble.calculate_price)
async def calculate_price(message: types.Message, state: FSMContext):
    try:
        price = int(message.text)
        # print(price)
        new_price = get_course_rub(price)
        # print(new_price)
        await message.answer(f"{price} RUB = {new_price} CNY")
        await message.answer(f"Нажмите /start, чтобы вернуться обратно")
        await state.clear()  # Очистить состояние после обработки
    except ValueError:
        await message.answer('Возникла ошибка, вероятно вы неправильно ввели данные. Вернитесь назад, нажав /start')


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        print("Bot's working has been started...")
        asyncio.run(main())
    except Exception as e:
        print(f"Something is going wrong: {e}")
