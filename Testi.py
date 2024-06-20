import random
import string
from random import randint, choice
from telebot import TeleBot


TOKEN = '7019757953:AAHpFEK_8l0E0E40-WGPHIl3qwibULDu-kE'
bot = TeleBot(TOKEN)

@bot.message_handler()
def start(message):
    if message.text == 'как дела?':
        bot.send_message(message.chat.id, 'Хорошо. а тебя?')
        return
    if message.text == 'что делаешь?':
        bot.send_message(message.chat.id, 'Тебя')
        return
    if message.text == 'пошути':
        bot.send_message(message.chat.id, 'Я расскажу вам шутку, как омар попал в маршрутку')
        return

def generate_name(length: int=10) -> str:
    aplphabet = string.ascii_lowercase + string.digits

    name = "".join(random.choice(aplphabet) for _ in range(length))

    name += "_bot"
    return name 

bot.polling(non_stop=True)