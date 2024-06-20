from telebot import TeleBot
from random import choice


TOKEN = '6832588484:AAH608vfLB9sl4tZOkzomSBmxuSsvkhux58'

bot = TeleBot(TOKEN)

class Game:
    comp = 0
    user = 0

    def update(self, user_winner: bool):
        if user_winner:
            self.user += 1
            return "Убедил"
        self.comp += 1
        return "Не убедил"
    
    def reset(self):
        self.comp = 0
        self.user = 0

gm = Game()

game_choice = ["камень", "ножницы", "бумага"]


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, f"Привет {message.from_user.username}!\nЧтобы начать играц отправь действие (камень, ножницы, А4)")

@bot.message_handler(func=lambda x: x.text.lower() in game_choice)
def game(message):
    global user_points
    global comp_points

    user_choice = message.text.lower()
    bot_choice = choice(game_choice)
    bot.send_message(message.chat.id, bot_choice
                     )
    if user_choice == 'камень' and bot_choice == 'ножницы':
        msg = gm.update(True)
    elif user_choice == 'бумага' and bot_choice == 'камень':
        msg = gm.update(True)
    elif user_choice == 'ножницы' and bot_choice == 'бумага':
        msg = gm.update(True)
    elif user_choice == bot_choice:
        msg = 'договорились, @everyone боты'
    else:
        msg = gm.update(False)
    bot.send_message(message.chat.id, msg)

@bot.message_handler(commands=['points'])
def get_points(message):
    bot.send_message(message.chat.id, f"Бот: {comp_points}\nИгрок: {user_points}")

@bot.message_handler(commands=['reset'])
def reset(message):
    global user_points
    global comp_points
    user_points = 0
    comp_points = 0
    bot.send_message(message.chat.id, "Бал обнулён")


bot.polling(non_stop=True)