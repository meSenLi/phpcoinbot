import calculation
import os
import telebot

BOT_TOKEN = os.environ.get('BOT_TOKEN')

bot = telebot.TeleBot(BOT_TOKEN)


def handle(addresses=None):
    data = calculation.calculation(addresses)
    string = ""
    for key in data.keys():
        if not addresses:
            string = string + key + "\n"
        else:
            string = string + "  "
        if isinstance(data[key], str):
            string = string + data[key] + "\n\n"
            continue
        for k in data[key]:
            string = string + "  " + \
                str(k) + " : " + str(data[key][k]) + "\n"
        string = string + "\n"
    return string


@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, "Howdy, how are you doing?")


@bot.message_handler(commands=['report'])
def send_welcome(message):
    bot.reply_to(message, handle())


@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    # print(message.text)
    bot.reply_to(message, handle(message.text))


bot.infinity_polling()
