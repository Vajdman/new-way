import telebot

from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import pprint

url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
parameters = {
  'slug':'bitcoin',
  'convert':'USD'
}
headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': '97d7c5b4-994f-4b3b-8f50-add1367ac6c0',
}

bot = telebot.TeleBot('2040507585:AAHYsEXXTzP0NE7DaeQfElbN84KVMdPk2lE')

@bot.message_handler(commands = ['start'])
def start(message):
   msg = bot.reply_to(message, """\
    Hi there, I am a Bitcoin Price Detecting bot.
    What's the selling price?
    """)

   bot.register_next_step_handler(msg, hello)

def hello(message, headers = headers, parameters = parameters, url = url):
  session = Session()
  session.headers.update(headers)

  selling_price = float(message.text)

  sold = False

  while not sold:
    try:
      response = session.get(url, params=parameters)

      name = json.loads(response.text)['data']['1']['name']
      price = json.loads(response.text)['data']['1']['quote']['USD']['price']

    except (ConnectionError, Timeout, TooManyRedirects) as e:
      print(e)

    if(price>selling_price):
      bot.send_message(message.chat.id, name + ": " + str(price) + "\nSELL THAT SHIT!")
      sold = True

bot.polling()
