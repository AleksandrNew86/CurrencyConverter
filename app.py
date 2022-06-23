import telebot

from config import *
from extensions import GottenCurrency, APIException
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message: telebot.types.Message):
    text = 'Введите сообщение боту в виде: \n\
 <имя валюты, цену которой вы хотите узнать> \
<имя валюты, в которой надо узнать цену первой валюты> \
<количество первой валюты>\n\
При вводе команды /value выводится информация о всех доступных валютах'
    bot.reply_to(message, text)


@bot.message_handler(commands=['value'])
def handle_value(message: telebot.types.Message):
    text = 'Доступныe для конвертации валюты:'
    for i in available_currency:
        text = text + f'\n- {str(i)}'
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def convert_currency(message):
    try:
        gotten_data = message.text.lower().split()
        if len(gotten_data) != 3:
            raise APIException("Неверное количество переменных!")
        base, quote, amount = gotten_data
        request_currency, from_, to_, amount = GottenCurrency.get_price(base, quote, amount)
        text = f'Результат конверсии: {amount} {from_} = {request_currency} {to_}'
    except APIException as e:
        bot.send_message(message.chat.id, f'Неправильно введены данные:\n{e}')
    except Exception as e:
        bot.send_message(message.chat.id, f'Непредвиденная ошибка:\n{e}')
    else:
        bot.send_message(message.chat.id, text)


bot.polling()
