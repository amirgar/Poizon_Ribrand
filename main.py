import logging
from random import randint
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types.input_file import FSInputFile

from config import TOKEN, CHANNEL_ID
import asyncio
import os
from valute_translator import get_course_rub

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher()

try:
    os.mkdir("users")
except Exception:
    pass


class Uyan(StatesGroup):
    calculate_price = State()


class Ruble(StatesGroup):
    calculate_price = State()


class Certificate(StatesGroup):
    name = State()
    phone_number = State()
    price = State()


class Order(StatesGroup):
    scrin = State()
    link = State()
    price = State()
    adress = State()
    name = State()
    size = State()
    phone_number = State()
    ready = State()


KEYBOARD_START = [
    [types.KeyboardButton(text="ОФОРМИТЬ ЗАКАЗ🛍"), types.KeyboardButton(text="СОЗДАТЬ СЕРТИФИКАТ🎁")],
    [types.KeyboardButton(text="ПЕРЕВЕСТИ ЮАНИ В РУБЛИ💴")],
]

KEYBOARD_BACK = [
    [types.KeyboardButton(text="ВЕРНУТЬСЯ ОБРАТНО⬅️")],
]

KEYBOARD_PRICES = [
    [types.KeyboardButton(text="1000₽"), types.KeyboardButton(text="2500₽"), types.KeyboardButton(text="4000₽")],
    [types.KeyboardButton(text="5000₽"), types.KeyboardButton(text="7500₽"), types.KeyboardButton(text="10000₽")]
]


@dp.message(Command('start'))
async def start_message(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=KEYBOARD_START,
        resize_keyboard=True,
        input_field_placeholder="Нажмите на необходимую кнопку"
    )
    photo = FSInputFile("logo.png", filename=os.path.basename("logo.png"))
    await bot.send_photo(message.chat.id, photo=photo)
    await message.answer('Добро пожаловать! Данный тг бот поможет вам оформить заказ с Poizon. Нажмите на '
                         'одну из кнопок ниже для продолжения работы:', reply_markup=keyboard)


@dp.message(F.text.lower() == "вернуться обратно⬅️")
async def start_message(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=KEYBOARD_START,
        resize_keyboard=True,
        input_field_placeholder="Выберите кнопку"
    )
    photo = FSInputFile("logo.png", filename=os.path.basename("logo.png"))
    await bot.send_photo(message.chat.id, photo=photo)
    await message.answer('Добро пожаловать! Данный тг бот поможет вам оформить заказ с Poizon. Нажмите на '
                         'одну из кнопок ниже для продолжения работы:', reply_markup=keyboard)


@dp.message(F.text.lower() == "помощь")
async def help_message(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=KEYBOARD_BACK,
        resize_keyboard=True
    )
    await message.answer('Здесь будет размещена помощь', reply_markup=keyboard)


@dp.message(F.text == "ПЕРЕВЕСТИ ЮАНИ В РУБЛИ💴")
async def calculate_price_start(message: types.Message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=KEYBOARD_BACK,
        resize_keyboard=True
    )
    await message.answer('Введите цену товара в юанях, я переведу Вам в рубли', reply_markup=keyboard)
    await state.set_state(Uyan.calculate_price)


@dp.message(Uyan.calculate_price)
async def calculate_price(message: types.Message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=KEYBOARD_BACK,
        resize_keyboard=True
    )
    try:
        price = int(message.text)
        print(price)
        new_price = get_course_rub(price)
        print(new_price)
        await message.answer(f"{price}¥ = {new_price}₽", reply_markup=keyboard)
        await state.clear()  # Очистить состояние после обработки
    except Exception:
        pass


@dp.message(F.text == "ОФОРМИТЬ ЗАКАЗ🛍")
async def make_order(message: types.Message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=KEYBOARD_BACK,
        resize_keyboard=True
    )
    id = str(message.chat.id)
    try:
        os.rmdir(f"users/{id}")
    except Exception:
        pass
    try:
        os.mkdir(f"users/{id}")
    except Exception:
        pass
    photo = FSInputFile(f'warning_first.jpg.', filename=os.path.basename("warning_first.jpg"))
    await bot.send_photo(message.chat.id, photo=photo)
    photo = FSInputFile(f'warning_second.jpg', filename=os.path.basename("warning_second.jpg"))
    await bot.send_photo(message.chat.id, photo=photo)
    await bot.send_message(message.chat.id,
                           "❗ Мы не принимаем заказы с товарами с таким знаком, как на первом фото. Также принимаем только те заказы, кнопки которых подсвечиваются только голубым и черным ❗")
    photo = FSInputFile(f'example_scrin.jpg', filename=os.path.basename("example_scrin.jpg"))
    await bot.send_photo(message.chat.id, photo=photo)
    await bot.send_message(message.chat.id, "Пожалуйста, вставьте фото товара, как показано на примере 🙌",
                           reply_markup=keyboard)
    await state.set_state(Order.scrin)


@dp.message(Order.scrin)
async def make_order(message: types.Message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=KEYBOARD_BACK,
        resize_keyboard=True
    )
    if message.photo:
        file_name = f"users/{message.chat.id}/order_photo.png"
        await bot.download(message.photo[-1], destination=file_name)

        photo = FSInputFile(f'example_link.jpg', filename=os.path.basename("example_link.jpg"))
        await bot.send_photo(message.chat.id, photo=photo)
        await bot.send_message(message.chat.id,
                               "Пожалуйста, отправьте ссылку на товар, взяв ее также, как показано на примере 📦",
                               reply_markup=keyboard)
        await state.set_state(Order.link)


@dp.message(Order.link)
async def make_order(message: types.Message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=KEYBOARD_BACK,
        resize_keyboard=True
    )
    try:
        with open(f'users/{message.chat.id}/order.txt', "w") as file:
            file.truncate(0)
            file.write(f"Ссылка на товар: {message.text}\n")
    except Exception:
        pass
    await bot.send_message(message.chat.id, "Напишите, пожалуйста, адрес доставки товара 🏠",
                           reply_markup=keyboard)
    await state.set_state(Order.adress)


@dp.message(Order.adress)
async def make_order(message: types.Message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=KEYBOARD_BACK,
        resize_keyboard=True
    )
    try:
        with open(f'users/{message.chat.id}/order.txt', "a") as file:
            file.write(f"Адрес доставки: {message.text}\n")
    except Exception:
        pass
    await bot.send_message(message.chat.id, "Введите Ваше ФИО 🖋️",
                           reply_markup=keyboard)
    await state.set_state(Order.name)


@dp.message(Order.name)
async def make_order(message: types.Message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=KEYBOARD_BACK,
        resize_keyboard=True
    )
    try:
        with open(f'users/{message.chat.id}/order.txt', "a") as file:
            file.write(f"ФИО: {message.text}\n")
    except Exception:
        pass
    await bot.send_message(message.chat.id,
                           "Если необходимо, то выберите размер товара (например: обуви). Если данная информация не нужна, поставьте прочерк",
                           reply_markup=keyboard)
    await state.set_state(Order.size)


@dp.message(Order.size)
async def make_order(message: types.Message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=KEYBOARD_BACK,
        resize_keyboard=True
    )
    try:
        with open(f'users/{message.chat.id}/order.txt', "a") as file:
            file.write(f"Размер: {message.text}\n")
    except Exception:
        pass
    await bot.send_message(message.chat.id, "Введите ваш номер телефона 📱",
                           reply_markup=keyboard)
    await state.set_state(Order.phone_number)


@dp.message(Order.phone_number)
async def make_order(message: types.Message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=KEYBOARD_BACK,
        resize_keyboard=True
    )
    try:
        with open(f'users/{message.chat.id}/order.txt', "a") as file:
            file.write(f"Номер  телефона: {message.text}\n")
            try:
                file.write(f"Тг пользователя: @{message.from_user.username}\n")
            except Exception:
                file.write("Тг пользователя не указано в приложении")
    except Exception:
        pass
    photo = FSInputFile(f'users/{message.chat.id}/order_photo.png', filename=os.path.basename("order_photo.png"))
    await bot.send_photo(message.chat.id, photo=photo)
    await bot.send_photo(CHANNEL_ID, photo=photo)
    order_text = ""
    with open(f'users/{message.chat.id}/order.txt', 'r') as file:
        order_text = file.read()
    await bot.send_message(CHANNEL_ID, order_text)
    await bot.send_message(message.chat.id, order_text)

    await bot.send_message(message.chat.id,
                           "Ваша заявка сформирована и отправлена! Скоро с Вами свяжется наш менеджер. Чтобы вернуться назад, нажмите на кнопку ниже",
                           reply_markup=keyboard)
    await state.clear()


"""
@dp.message(F.text == "НАЦЕНКА ЗА ДОСТАВКУ🚚")
async def price_order(message: types.message):
    with open("price_orders.txt", "r", encoding="UTF-8") as file:
        await bot.send_message(message.chat.id, file.read())
"""


@dp.message(F.text == "СОЗДАТЬ СЕРТИФИКАТ🎁")
async def certificate_order(message: types.message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=KEYBOARD_PRICES,
        resize_keyboard=True
    )
    with open("certificate_order", 'r', encoding="UTF-8") as file:
        await bot.send_message(message.chat.id, file.read())
    await bot.send_message(message.chat.id, "Выберите сумму сертификата 💵", reply_markup=keyboard)
    await state.set_state(Certificate.price)


@dp.message(Certificate.price)
async def certiicate_order(message: types.message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=KEYBOARD_BACK,
        resize_keyboard=True
    )
    with open(f'users/{message.chat.id}/certificate.txt', "w", encoding="UTF-8") as file:
        file.truncate(0)
    with open(f'users/{message.chat.id}/certificate.txt', "a", encoding="UTF-8") as file:
        file.write(f"Summ certificate: {message.text[:-1]}\n")
    await bot.send_message(message.chat.id, "Введите ФИО, на него будет оформлен сертификат", reply_markup=keyboard)
    await state.set_state(Certificate.name)


@dp.message(Certificate.name)
async def certiicate_order(message: types.message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=KEYBOARD_BACK,
        resize_keyboard=True
    )
    try:
        with open(f'users/{message.chat.id}/certificate.txt', "a") as file:
            file.write(f"ФИО оформляющего: {message.text}\n")
    except Exception:
        pass
    await bot.send_message(message.chat.id, "Введите Ваш номер телефона", reply_markup=keyboard)
    await state.set_state(Certificate.phone_number)


@dp.message(Certificate.phone_number)
async def certiicate_order(message: types.message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=KEYBOARD_BACK,
        resize_keyboard=True
    )
    code = randint(1000000, 10000000)
    try:
        with open(f'users/{message.chat.id}/certificate.txt', "a") as file:
            file.write(f"Номер телефона: {message.text}\n")
            file.write(f"Код серификата: {code}\n")
            file.write(f"Тг покупателя: @{message.from_user.username}\n")
    except Exception:
        pass
    try:
        with open(f'users/{message.chat.id}/certificate.txt', 'r') as file:
            order_text = file.read()
        await bot.send_message(CHANNEL_ID, f'СЕРТИФИКАТ\n{order_text}')
        await bot.send_message(message.chat.id,
                               f'{order_text}✅ Заявка на создание сертификата подана! Скоро с Вами свяжется менеджер для оплаты')
    except Exception:
        pass
    await bot.send_message(message.chat.id,
                           "❗ВАЖНО❗\nЗапомните код сертификата, без него мы не сможем выдать сертификат получателю!",
                           reply_markup=keyboard)
    await state.clear()


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        print("Bot's working has been started...")
        asyncio.run(main())
    except Exception as e:
        print(f"Something is going wrong: {e}")
