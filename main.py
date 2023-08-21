import telebot

from config import keys, TOKEN
from extensions import APIException, GetPrice

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def start(message: telebot.types.Message):
    text = 'Для начала работы введите комманду в следующем формате:\n' \
           '<Наименование валюты>' \
           '<В какую валюту перевести> ' \
           '<Количество переводимой валюты>\n' \
           'Перечень доступных валют: /values\n' \
           'Пример правильного запроса: /example'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def start(message: telebot.types.Message):
    text = 'Доступные валюты: '
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)


@bot.message_handler(commands=['example'])
def start(message: telebot.types.Message):
    text = '<Что><Куда><Сколько>\nбиткоин эфириум 0.1'
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        bot.reply_to(message, GetPrice.converter(message.text.split(' ')))
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду.\n{e}')


bot.polling()
