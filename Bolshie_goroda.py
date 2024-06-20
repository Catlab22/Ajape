from telebot import TeleBot
import logging
from random import choice
from functools import wraps

logging.basicConfig(filename="user_logs.txt", encoding="utf-8", level=logging.INFO, format="%(asctime)s - %(message)s")

TOKEN = '7080325580:AAG0BKmbJyze1SP9oIIj121GbQdpSZPZhSQ'
bot = TeleBot(TOKEN)
used_words = []
letter = ""
game = False

def user_action(func):
    @wraps(func)
    def wrapper(message, *args, **kwargs):
        user = message.from_user.id
        command = message.text
        logging.info(f"User:{user}, Command: {command}")
        return func(message, *args, **kwargs)
    return wrapper    

with open("cities.txt", "r", encoding="utf-8") as file:
    cities = [word.strip().lower() for word in file.readlines()]

def select_letter(text: str) -> str:
    i = 1
    while text[-1*i] in ("ь", "ъ", "ы", "й"):
        print(text[-1*i])
        i += 1
    return text [-1*i]

@bot.message_handler(commands=['start'])
@user_action
def start(message):
    bot.send_message(message.chat.id,
                     f"Привет {message.from_user.username}! Я бот.(/goroda). [кстати, я записываю твои сообщения. Если ТЫ с этим не согласен, то перестань меня использовать]")
    
@bot.message_handler(commands=['goroda'])
@user_action
def game(message):
    global game
    global letter
    game = True
    city = choice(cities)
    letter = select_letter(city)
    bot.send_message(message.chat.id, city)

@bot.message_handler()
@user_action
def play(message):
    global game
    global used_words
    global letter
    if game:
        if message.text.lower() in used_words:
            bot.send_message(message.chat.id, "назван")
            return
        if message.text.lower()[0] != letter:
            bot.send_message(message.chat.id, "непрвильно")
            return
        if message.text.lower() in cities:
            letter = select_letter(message.text.lower())
            used_words.append(message.text.lower())
            for city in cities:
                if city[0] == letter and city not in used_words:
                    letter = select_letter(city)
                    bot.send_message(message.chat.id, city)
                    used_words.append(city)
                    return
            bot.send_message(message.chat.id, "- Я")
            game = False
            return
        bot.send_message(message.chat.id, "Нету такого")


bot.polling(non_stop=True, interval=1)