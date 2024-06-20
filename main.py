from telebot import TeleBot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, Message
import db
from time import sleep
from random import choice
#[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]
TOKEN = "7481073878:AAFyPGixa9qcZmQlRl91XbjD2lSPZohT7ZM"
bot = TeleBot(TOKEN)
#[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]
game = False
night = False
#[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]
def get_killed(night: bool) -> str | None:
    if not night:
        username_killed = db.citizen_kill()
        return f"Горожане... {username_killed}" 
    username_killed = db.mafia_kill()
    return f"Мафия... {username_killed}"
#[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]
def autoplay_citizen(message: Message):
    players_roles = db.get_players_roles()
    for player_id, _ in players_roles:
        usernames = db.get_all_alive()
        name = f"roboto{player_id}"
        if player_id < 5 and name in usernames:
            usernames.remove(name)
            vote_username = choice(usernames)
            db.vote("citizen_vote", vote_username, player_id)
#[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]
def game_loop(message: Message):
    global night, game
    bot.send_message(message.chat.id, "Драсте, Зубенко Михаил Петрович")
    sleep(60)
    while True:
        msg = get_killed(night)
        bot.send_message(message.chat.id, msg)
        if not night:
            bot.send_message(message.chat.id, "Суп кипит, город спит")
        else:
            bot.send_message(message.chat.id, "Суп кипит, мафия спит")
        winner = db.check_winner()
        if winner == "Мафия..." or winner == "Горожане...":
            game = False
            bot.send_message(message.chat.id, f"Игра кончена(-я) убедили: {winner}")
            return
        db.clear(dead=False)
        night = not night
        alive = db.get_all_alive()
        alive = "\n".join(alive)
        bot.send_message(message.chat.id, "в игре:\n{alive}")
#[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]
@bot.message_handler(func=lambda message: message.text.lower() == "всегда готов..." and message.chat.type == "private")
def send_text(message: Message):
    bot.send_message(message.chat.id, f"{message.from_user.first_name} игрует")
    bot.send_message(message.chat.id, "Вас приняли")
    db.insert_player(message.from_user.id, message.from_user.first_name)
#[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]
@bot.message_handler(commands=["start"])
def game_on(message: Message):
    if not game:
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(KeyboardButton("всегда готов..."))
        bot.send_message(message.chat.id, "Жми ЗТЕ Блэт", reply_markup=keyboard)
#[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]
@bot.message_handler(commands=['play'])
def game_start(message: Message):
    global game
    players = db.players_amount()
    if players >= 5 and not game:
        db.set_roles(players)
        players_roles = db.get_players_roles()
        mafia_usernames = db.get_mafia_usernames()
        for player_id, role in players_roles:
            try:
                bot.send_message(player_id, role)
            except Exception:
                continue
            
            if role == "mafia":
                bot.send_message(player_id, f"все члены... мафии!(лучше не стало):\n{mafia_usernames}")
        game = True
        bot.send_message(message.chat.id, "поплыли(ага, блин, под грибами, что ли?!)")
    else:
        bot.send_message(message.chat.id, "Мало простолюдин (кому тогда быть мафиозником?)")
        for i in range(5 - players):
            bot_name = f"robot{i}"
            db.insert_player(i, bot_name)
            bot.send_message(message.chat.id, f"{bot_name} ботяра появился")
            sleep(0.2)
        game_start(message)
#[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]
@bot.message_handler(commands=['kick'])
def kick(message: Message):
    username = ' '.join(message.text.split(" ")[1:])
    usernames = db.get_all_alive()
    if not night:
        if not username in usernames:
            bot.send_message(message.chat.id, "Нету человека")
            return
        voted = db.vote("citizen_vote", username, message.from_user.id)
        if voted:
            bot.send_message(message.chat.id, "Голос учитан")
            return
        bot.send_message("Голос учитан (нет)")
#[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]
@bot.message_handler(commands=['kill'])
def kill(message: Message):
    username = ' '.join(message.text.split(" ")[1:])
    usernames = db.get_all_alive()
    mafia_usernames = db.get_mafia_usernames()
    if night and message.from_user.first_name in mafia_usernames:
        if not username in usernames:
            bot.send_message(message.chat.id, "Нету человека")
            return
        voted = db.vote("mafia_vote", username, message.from_user.id)
        if voted:
            bot.send_message(message.chat.id, "Голос учитан")
            return
        bot.send_message("Нельзя")
    bot.send_message(message.chat.id, "Сейчас нельзя")
#[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]
bot.polling(non_stop=True, interval=1)