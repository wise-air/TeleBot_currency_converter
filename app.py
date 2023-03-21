import telebot
from config import keys, TOKEN
from classes import ConvertionExeption, CryptoConverter, InlineKeyboard


bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Для того чтобы выполнить конвертацию валют, напишите команду боту в виде:\n ' \
           '<имя валюты> <имя валюты для конвертации> <количество конвертируемой валюты>\n ' \
           'или выберите пару валют + сумму для конвертации с экранной клавиатуры ' \
           'перейдя по ссылке  -> /values\n' \
           '(НАПРИМЕР: рубль юань 50)'

    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты для конвертации:\n'
    for key in keys.keys():
        text = ' ->'.join((text, key, ))

    bot.send_message(message.chat.id, text, reply_markup=InlineKeyboard.keyboard)

def getmessage(message):
    if InlineKeyboard.value == '':
        bot.send_message(message.from_user.id, "Выберете пару валют для конвертации затем сумму", reply_markup=InlineKeyboard.keyboard)
    else:
        bot.send_message(message.from_user.id, InlineKeyboard.value, reply_markup=InlineKeyboard.keyboard)

@bot.callback_query_handler(func=lambda call: True)
def callback_func(query):
    data = query.data

    if data == '=':
        try:
            values1 = InlineKeyboard.value.split()
            quote, base, amount = values1
            total_base = CryptoConverter.get_price(quote.lower(), base.lower(), amount)
            exch = float(total_base) * float(amount)
            text = f'Цена {amount} {quote.lower()} в {base.lower()} равна %99.2f {base.lower()}' % (exch)
            bot.edit_message_text(chat_id=query.message.chat.id, message_id=query.message.message_id, text=text, reply_markup=InlineKeyboard.keyboard)

        except:
            InlineKeyboard.value = 'Ошибка! Введите повторно!'
            text2 = 'Выберете пару валют для конвертации, затем сумму'
            bot.answer_callback_query(callback_query_id=query.id, text=text2)

    elif data == 'C':
        InlineKeyboard.value = ''

    else:
        InlineKeyboard.value += data

    if InlineKeyboard.value != InlineKeyboard.old_value:
        if InlineKeyboard.value == '':
            bot.edit_message_text(chat_id=query.message.chat.id, message_id=query.message.message_id, text="0", reply_markup=InlineKeyboard.keyboard)
        else:
            bot.edit_message_text(chat_id=query.message.chat.id, message_id=query.message.message_id, text=InlineKeyboard.value, reply_markup=InlineKeyboard.keyboard)

    InlineKeyboard.old_value = InlineKeyboard.value
    if InlineKeyboard.value == 'Ошибка! Введите повторно!': InlineKeyboard.value = ''

@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split()
        if len(values) != 3:
            raise ConvertionExeption('Вы ввели лишние или  недостаточные параметры! Повторите запрос')

        quote, base, amount = values
        total_base = CryptoConverter.get_price(quote.lower(), base.lower(), amount)
    except ConvertionExeption as e:
        bot.reply_to(message, f'Ошибка:\n{e}')

    except Exception as e:
        bot.reply_to(message, f'Непредвиденная ошибка:\n{e}')
    else:
        exch = float(total_base) * float(amount)
        text = f'Цена {amount} {quote.lower()} в {base.lower()} равна %99.2f {base.lower()}' % (exch)
        bot.send_message(message.chat.id, text)

if __name__ == '__main__':
    bot.polling()
