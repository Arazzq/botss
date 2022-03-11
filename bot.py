import telebot
import random
from telebot import types
mafia_count = 0
city_count = 0
count_num = 0
roles = 0


token = '5170940542:AAFe0QKhQe76c3NMfrvk5rJo3AeEA7o9orM'
bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def start(message):
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    keyboard.add(*[types.KeyboardButton(choice) for choice in ['Hə', 'Yox']])
    ans = bot.send_message(message.chat.id,
                           "Salam! Yaxşı nə, Mafia oynuyacağıq?",
                           reply_markup=keyboard)
    bot.register_next_step_handler(ans, choicecheck)


def choicecheck(message):
    if message.text == 'Hə':
        accepted(message)
    else:
        declined(message)


def declined(message):
    bot.send_message(message.chat.id, "Heyf, əgər belədirsə - Danış, Mən Gözləyirəm")


def accepted(message):
    ans = bot.send_message(message.chat.id, "Sərindir! Yaxşı, sonra qərar verək, Neçə nəfər oynuyacaq?")
    bot.register_next_step_handler(ans, count)


def count(message):
    global count_num, mafia_count, city_count
    count_num = int(message.text)
    mafia_count = count_num / 3
    city_count = count_num - mafia_count
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    keyboard.add(*[types.KeyboardButton(roles) for roles in
                   ["Кlassik: Маfiya və şəhər", "Кlassik с комissarlar", "Кlassik və Don",
                    "Klassik və Komissar və Don"]])
    msg = bot.send_message(message.chat.id,
                           "Sərindir, İndi isə rolları seçək",
                           reply_markup=keyboard)
    bot.register_next_step_handler(msg, rolescheck)

def rolescheck(message):
    global count_num, mafia_count, city_count, roles
    roles = 0
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    keyboard.add(*[types.KeyboardButton(finalchoice) for finalchoice in
                   ["Давай", "Yox, Başqa paylanmanı seçək"]])
    if message.text == "Кlassik: Маfiya və Şəhər":
        roles = 1
    if message.text == "Классика с комissar":
        roles = 2
    if message.text == "Классика с Don":
        roles = 3
    if message.text == "Классика с komissar və Don":
        roles = 4
    ans = bot.send_message(message.chat.id,
                           "Предлагаю тебе такой расклад: %s мафий, %s мирных" % (int(mafia_count), count_num - int(mafia_count)),
                           reply_markup=keyboard)
    bot.register_next_step_handler(ans, final_choice)


def final_choice(message):
    global count_num, mafia_count, city_count, roles
    if message.text == "Davay":
        createtable(message)
    else:
        msg = bot.send_message(message.chat.id, "Окey, Nə qədər mafiya olacaq?")
        bot.register_next_step_handler(msg, specificmafia)


def specificmafia(message):
    global count_num, mafia_count, city_count, roles
    mafia_count = int(message.text)
    createtable(message)


def createtable(message):
    global count_num, mafia_count, city_count, roles
    mafia_count = int(mafia_count)
    city_count = count_num - mafia_count
    city = []
    if roles == 1:
        for i in range(city_count):
            city.append(0)
        for i in range(city_count, city_count + mafia_count):
            city.append(1)
    elif roles == 2:
        for i in range(mafia_count):
            city.append(1)
        city.append(2)
        for i in range(mafia_count + 1, mafia_count + city_count):
            city.append(0)
    elif roles == 3:
        city.append(3)
        for i in range(1, mafia_count):
            city.append(1)
        for i in range(mafia_count, city_count):
            city.append(0)
    elif roles == 4:
        city.append(3)
        for i in range(1, mafia_count):
            city.append(1)
        city.append(2)
        for i in range(mafia_count + 1, mafia_count + city_count):
            city.append(0)
    random.shuffle(city)
    for i in range(count_num):
        s = "Oyun номер " + str(i+1) + " - "
        if city[i] == 0:
            bot.send_message(message.chat.id, s + "Mülki")
        elif city[i] == 1:
            bot.send_message(message.chat.id, s + "Маfiya")
        elif city[i] == 2:
            bot.send_message(message.chat.id, s + "Комissar")
        elif city[i] == 3:
            bot.send_message(message.chat.id, s + "Don")
    bot.send_message(message.chat.id, "Oyundan zövq alın!")
bot.polling()
