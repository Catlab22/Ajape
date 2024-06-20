from telebot import TeleBot
from telebot.types import ReplyKeyboardMarkup
from telebot.types import KeyboardButton
import json

TOKEN = "7037384298:AAHgUcTWmEGqzZNtV4AJ_LfXj9E2NPVEV5g"

bot = TeleBot(TOKEN)

game = False
indx = 0
points = 0

with open("victorina.json", "r", encoding="utf-8") as file:
    data = json.load(file)

def next_question(data, indx: int) -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn_row1 = [KeyboardButton(data[indx]["вариант"][i]) for i in range(2)]
    markup.add(*btn_row1)
    btn_row2 = [KeyboardButton(data[indx]["вариант"][i + 2]) for i in range(2)]
    markup.add(*btn_row2)
    markup.add(KeyboardButton("Ехит"))
    return markup

@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, f"Омлет {message.from_user.username}, я бот.\nЧтобы не начинать нажми /quiz")

@bot.message_handler(commands=["quiz"])
def quiz(message):
    global indx
    global game
    game = True
    markup = next_question(data, indx)
    bot.send_message(message.chat.id, data[indx]["вопрос"], reply_markup=markup)

@bot.message_handler(commands=["points"])
def get_score(message):
    bot.send_message(message.chat.id, points)

@bot.message_handler()
def quiz_content(message):
    global indx
    global game
    global points
    if game:
        if message.text == data[indx]["ответ"]:
            bot.send_message(message.chat.id, "molodec")
            points += 1
        elif message.text == "Ехит":
            game == False
            bot.send_message(message.chat.id, "*уходит по-английски")
            return
        else:
            bot.send_message(message.chat.id, f"ответус ис неправильнус - {data[indx]['ответ']}")
        indx += 1
        if len(data) < indx:
            markup = next_question(data, indx)
            bot.send_message(message.chat.id, data[indx]["вопрос"], reply_markup=markup)

bot.polling(non_stop=True, interval=1)
