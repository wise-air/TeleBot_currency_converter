import requests
import json
import telebot
from config import keys

class InlineKeyboard:
    value = ''
    old_value = ''

    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.row(   telebot.types.InlineKeyboardButton('Сбросить', callback_data='C')
                    )

    keyboard.row(   telebot.types.InlineKeyboardButton('Рубль ₽', callback_data='рубль '),
                    telebot.types.InlineKeyboardButton('Юань Ұ', callback_data='юань '),
                    telebot.types.InlineKeyboardButton('Доллар $', callback_data='доллар '),
                    telebot.types.InlineKeyboardButton('Евро €', callback_data='евро ')
                    )

    keyboard.row(   telebot.types.InlineKeyboardButton('6', callback_data='6'),
                    telebot.types.InlineKeyboardButton('7', callback_data='7'),
                    telebot.types.InlineKeyboardButton('8', callback_data='8'),
                    telebot.types.InlineKeyboardButton('9', callback_data='9')
                    )

    keyboard.row(   telebot.types.InlineKeyboardButton('2', callback_data='2'),
                    telebot.types.InlineKeyboardButton('3', callback_data='3'),
                    telebot.types.InlineKeyboardButton('4', callback_data='4'),
                    telebot.types.InlineKeyboardButton('5', callback_data='5')
                    )

    keyboard.row(   telebot.types.InlineKeyboardButton('.', callback_data='.'),
                    telebot.types.InlineKeyboardButton('00', callback_data='00'),
                    telebot.types.InlineKeyboardButton('0', callback_data='0'),
                    telebot.types.InlineKeyboardButton('1', callback_data='1')
                    )

    keyboard.row(   telebot.types.InlineKeyboardButton('Конвертировать', callback_data='=')
                    )

class ConvertionExeption(Exception):
    pass

class CryptoConverter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):

        if quote == base:
            raise ConvertionExeption(f'Вы ввели одинаковую валюту: "{base}"')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConvertionExeption(f'Не удалось обработать валюту: "{quote}"')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConvertionExeption(f'Не удалось обработать валюту: "{base}"')

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionExeption(f'Не удалось обработать конвертируемую сумму {amount}')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base = json.loads(r.content)[keys[base]]

        return total_base
