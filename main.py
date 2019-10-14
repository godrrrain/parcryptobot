from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import telebot


SLOVAR_KRYPT = {}
STRONG_KRYPT = ''
VSEGO_USD = 0
VSEGO_BTC = 0
CONDITION = 0
PEREM_SYMBOL = ''
USER_ID = 0


def __Init__():
    global SLOVAR_KRYPT, STRONG_KRYPT, VSEGO_USD, VSEGO_BTC, USER_ID
    print(STRONG_KRYPT)

    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
    parameters = {
        'symbol': STRONG_KRYPT
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': '*key*',
    }

    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(url, params=parameters)
        data = json.loads(response.text)
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)

    GetBobosi(data, SLOVAR_KRYPT)
    bot.send_message(USER_ID, "Твое состояние крипты в даларах: {}".format(VSEGO_USD))

    parameters = {
        'symbol': 'BTC'
    }
    session = Session()
    session.headers.update(headers)
    try:
        response = session.get(url, params=parameters)
        data = json.loads(response.text)
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)

    Convert_BTC(data, VSEGO_USD)
    bot.send_message(USER_ID, 'Вся твоя крипта в Биткоинах(BTC)(whoy?)(хуи): {}'.format(VSEGO_BTC))


def God_Strong(slov):
  global  STRONG_KRYPT
  for pisya in slov:
    STRONG_KRYPT += '{},'.format(pisya)
  STRONG_KRYPT = STRONG_KRYPT[:-1]


def GetBobosi(dannie, slovar):
    global  VSEGO_USD
    VSEGO_USD = 0
    for nahoi in slovar:
        print(nahoi)
        print("_______________________________________________")
        print(dannie)
        VSEGO_USD += (dannie['data'][nahoi]['quote']['USD']['price'] * float(slovar[nahoi]))


def Convert_BTC(dati, usd):
    global VSEGO_BTC
    VSEGO_BTC = usd / dati['data']['BTC']['quote']['USD']['price']


bot = telebot.TeleBot('*token*')


@bot.message_handler(func=lambda message: CONDITION == 1)
def chit_kript(message):
    global CONDITION, PEREM_SYMBOL
    if message.text == 'end':
        CONDITION = 0
        God_Strong(SLOVAR_KRYPT)
        __Init__()
    else:
        PEREM_SYMBOL = message.text
        bot.send_message(message.from_user.id, 'Введи количество {}: '.format(message.text))
        CONDITION = 2


@bot.message_handler(func=lambda message: CONDITION == 2)
def chit_value(message):
    global  CONDITION, SLOVAR_KRYPT, PEREM_SYMBOL
    SLOVAR_KRYPT[PEREM_SYMBOL] = message.text
    bot.send_message(message.from_user.id, 'Введи символ крипты(etc. BTC or ETH). Напиши слово "end", чтобы закончить считывание: ')
    CONDITION = 1


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    global CONDITION, USER_ID, STRONG_KRYPT
    if message.text == "Привет":
        STRONG_KRYPT = ''
        USER_ID = message.from_user.id
        bot.send_message(message.from_user.id, 'Введи символ крипты(etc. BTC or ETH): ')
        CONDITION = 1
        bot.send_message(message.from_user.id, "Иди нахуй лох Влад Пидарас кста")
    #if message.text == "да":
      #  bot.send_message(message.from_user.id, )
    if message. text == "Каво":
        bot.send_message(message.from_user.id, 'Таво блеат')
        __Init__()


bot.polling(none_stop=True)
