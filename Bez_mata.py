from telebot import TeleBot, types
from time import time
from random import randint


TOKEN = '7072330766:AAEU2waepOcIMT_A7k1o-MAa2RNryFOMDY0'
bot = TeleBot(TOKEN)

with open("Ignat_speech.txt", "r", encoding='utf-8') as file:
    data = [word.strip().lower() for word in file.readlines()]


def is_group(message) -> bool:
    return message.chat.type in ("group", "supergroup")

@bot.message_handler(commands=['check'])
def default_test(message):
    global sum_check

    keyboard = types.InlineKeyboardMarkup()
    numbers = ["1", "2", "3", "4", "5",
                "6", "7", "8", "9", "10"]
    keys = []
    for indx, number in enumerate(numbers):

        keys.append(types.InlineKeyboardButton(
            text=number, callback_data=indx+1))
    keyboard.row(*keys)

    n1 = randint(1, 5)
    n2 = randint(1, 5)
    sum_check = n1 + n2

    bot.send_message(
        message.chat.id, f"Реши пример: {n1} + {n2} = ?", reply_markup=keyboard)
    
@bot.callback_query_handler(func=lambda call: call.data)
def callback_inline(call):
    global sum_check
    if int(call.data) == sum_check:
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text="Проверен")
    if int(call.data) != sum_check:
        bot.ban_chat_member(call.message.chat.id,
                            call.from_user.id)

@bot.message_handler(func=lambda message: message.entities is not None and is_group(message))
def delete_links(message):
    for entity in message.entities:
        for entity.type in ["url", "text_link"]:
            bot.delete_message(message.chat.id, message.message_id)

def has_bad_words(text):
    message_words = text.split(' ')
    for word in message_words:
        if word in data:
            return True
    return False

@bot.message_handler(func=lambda message: has_bad_words(message.text.lower()) and is_group(message))
def bad_bad_words(message):
    bot.restrict_chat_member(
        message.chat.id,
        message.from_user.id,
        until_date=time()+1200)
    bot.send_message(message.chat.id, "Вы просрались", reply_to_message_id=message.message_id)
    bot.delete_message(message.chat.id, message.message_id)

bot.polling(non_stop=True, interval=1)