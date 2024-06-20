from telebot import TeleBot
from utils import random_duck, random_fox, random_dog

TOKEN = '6902674114:AAF3q_ulFs1ySKEQC0peXKo7vHUI5H-Gr-A'
bot = TeleBot(TOKEN)

@bot.message_handler(commands=['duck'])
def get_duck(message):
    img = random_duck()
    bot.send_message(message.chat.id, img)

@bot.message_handler(commands=['fox'])
def get_fox(message):
    img = random_fox()
    bot.send_message(message.chat.id, img)

@bot.message_handler(commands=['dog'])
def get_dog(message):
    img = random_dog()
    bot.send_message(message.chat.id, img)

bot.polling(non_stop=True)