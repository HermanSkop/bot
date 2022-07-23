import math

import telebot
from localStoragePy import localStoragePy
from telebot import types

import globals
from database import *
from globals import content

bot = telebot.TeleBot('')

localStorage = localStoragePy('telegram_bot_DC', 'json')

if localStorage.getItem('on_library_page') is None:
    localStorage.setItem('on_library_page', 0)


# rewrite if possible
def refresh_page():
    try:
        on_library_page = int(localStorage.getItem('on_library_page'))
        names_on_page = types.InlineKeyboardMarkup(row_width=1)
        for i in range(on_library_page * content, content * (on_library_page + 1)):
            name = definitions[i][0]
            button = types.InlineKeyboardButton(name, callback_data=name)
            names_on_page.add(button)
        names_on_page.row_width = 3
        if on_library_page != 0 and not on_last_page():
            prev_page = types.InlineKeyboardButton('⬅', callback_data='prev')
            menu = types.InlineKeyboardButton('Menu', callback_data='menu')
            next_page = types.InlineKeyboardButton('➡', callback_data='next')
            names_on_page.add(prev_page, menu, next_page)
        elif on_library_page == 0:
            menu = types.InlineKeyboardButton('Menu', callback_data='menu')
            next_page = types.InlineKeyboardButton('➡', callback_data='next')
            names_on_page.add(menu, next_page)
        elif on_last_page():
            menu = types.InlineKeyboardButton('Menu', callback_data='menu')
            prev_page = types.InlineKeyboardButton('⬅', callback_data='prev')
            names_on_page.add(prev_page, menu)
        else:
            menu = types.InlineKeyboardButton('Menu', callback_data='menu')
            return menu
        return names_on_page
    except Exception:
        localStorage.setItem('on_library_page', 0)



def to_next_page(message):
    globals.on_library_page += 1
    localStorage.setItem('on_library_page', int(localStorage.getItem('on_library_page')) + 1)
    update_curr_page(message)


def to_prev_page(message):
    globals.on_library_page -= 1
    localStorage.setItem('on_library_page', int(localStorage.getItem('on_library_page')) - 1)
    update_curr_page(message)


def on_last_page():
    on_library_page = int(localStorage.getItem('on_library_page'))
    if on_library_page == 0 and number_of_definitions <= content:
        return True
    elif (math.ceil(number_of_definitions / content) - 1) == on_library_page:
        return True
    else:
        return False


def get_definition_in_form(name):
    return '🔸 ' + name + '\n\n📖 ' + get_description(name) + '\n\n🌐 Development Corporation ®'


# outputs the whole library
def show_library(message):
    print_curr_page(message)


# outputs main menu
@bot.callback_query_handler(func=lambda call: check_menu(call.data))
def return_to_menu(call):
    if call.data == 'menu':
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        start(call.message)
    elif call.data == 'prev':
        to_prev_page(call.message)
    elif call.data == 'next':
        to_next_page(call.message)
    bot.answer_callback_query(call.id, text='menu')


def delete_previous_library():
    try:
        bot.delete_message(chat_id=localStorage.getItem('last_library_chat_id'),
                           message_id=localStorage.getItem('last_library_message_id'))
    except Exception:
        print('No such chat exists')


def print_curr_page(message):
    delete_previous_library()
    last_library_message = bot.send_message(chat_id=message.chat.id, text='Библиотека',
                                            reply_markup=refresh_page())
    print(last_library_message)
    localStorage.setItem('last_library_chat_id', last_library_message.chat.id)
    localStorage.setItem('last_library_message_id', last_library_message.message_id)


def update_curr_page(message):
    bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text='Библиотека',
                          reply_markup=refresh_page())


@bot.inline_handler(func=lambda query: len(query.query) > 0)
def show_list(query):
    results = []
    id = 0
    for name in definitions:
        if query.query.lower() in name[0].lower():
            results.append(
                types.InlineQueryResultArticle(
                    id=str(id), title=name[0],
                    description=name[1],
                    input_message_content=types.InputTextMessageContent(
                        message_text=get_definition_in_form(name[0])))
            )
            id += 1
    bot.answer_inline_query(query.id, results, cache_time=1)


# check_name checks if the given name in names of definitions`
def check_name(name):
    for definition in definitions:
        if definition[0] == name:
            return True
    return False


@bot.callback_query_handler(func=lambda call: check_name(call.data))
def show_definition(call):
    bot.send_message(call.message.chat.id, get_definition_in_form(call.data))
    bot.answer_callback_query(call.id, text=call.data)


# check_menu checks if the given text is menu or left/right button
def check_menu(text):
    if text == 'menu' or text == 'prev' or text == 'next':
        return True
    else:
        return False


@bot.message_handler(commands=["start"])
def start(message):
    delete_previous_library()
    send_mess = f'Здравствуйте, {message.from_user.first_name} {message.from_user.last_name}!\n' \
                f'Да начнётся ваше изучение терминов из нашей библиотеки!\n' \
                f'/library - команда активирует режим поиска по библиотеке\n' \
                f'/help - команда вызывает список команд\n' \
                f'/start - Запускает бота\n' \
                f'@Test_crypto_doc_bot'
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row_width = 2
    btn1 = types.KeyboardButton("📚 ТЕРМИНЫ 📚")
    btn2 = types.KeyboardButton("📈 ФИГУРЫ 📉")
    btn3 = types.KeyboardButton("🗞 НОВОСТИ 🗞")
    btn4 = types.KeyboardButton("⚡ START ⚡")

    markup.add(btn1, btn2, btn3, btn4)
    bot.send_message(message.chat.id, send_mess, reply_markup=markup)


@bot.message_handler(commands=["help"])
def help(message):
    send_mess = f'Похоже, вам понадобилась помощь, так что держите список возможных команд:\n' \
                f'/libsearch - команда активирует режим поиска по библиотеке\n' \
                f'/help - команда вызывает список команд\n' \
                f'/start - Запускает бота\n' \
                f'На этом пока что всё, так что удачи в использовании нашего бота!'
    bot.send_message(message.chat.id, send_mess, parse_mode='html')


@bot.message_handler(content_types=['text'])
def main_menu(message):
    if message.text == "📚 ТЕРМИНЫ 📚":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("🧑‍🎓 ОБУЧЕНИЕ 👩‍🎓")
        btn2 = types.KeyboardButton("🧑‍💻 ПРОВЕРЬ СЕБЯ 👩‍💻")
        btn3 = types.KeyboardButton("🔎 ПОИСК 🔎")
        btn4 = types.KeyboardButton("📋 ИНСТРУКЦИЯ 📋")
        btn5 = types.KeyboardButton("🔄 RESTART 🔄")

        markup.add(btn1, btn2, btn3, btn4, btn5)
        bot.send_message(message.chat.id, 'Выберите действие', reply_markup=markup)
    elif message.text == "📈 ФИГУРЫ 📉":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("📕 ОБУЧЕНИЕ 📗")
        btn2 = types.KeyboardButton("📊 ПРОВЕРЬ СЕБЯ 📊")
        btn3 = types.KeyboardButton("🔎 ПОИСК 🔎")
        btn4 = types.KeyboardButton("🧭 ИНСТРУКЦИЯ 🧭")
        btn5 = types.KeyboardButton("🔄 RESTART 🔄")

        markup.add(btn1, btn2, btn3, btn4, btn5)
        bot.send_message(message.chat.id, 'Выберите действие', reply_markup=markup)
    elif message.text == "🗞 НОВОСТИ 🗞":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("📒 ИНФОРМАЦИЯ 📒")
        btn2 = types.KeyboardButton("🎞 ИНСТРУКЦИЯ 🎞")
        markup.row_width = 2
        btn3 = types.KeyboardButton("🔄 RESTART 🔄")

        markup.add(btn1, btn2, btn3)
        bot.send_message(message.chat.id, 'Выберите действие', reply_markup=markup)
    elif message.text == "🧑‍💻 ПРОВЕРЬ СЕБЯ 👩‍💻":
        bot.send_message(message.chat.id, 'Выберите действие', parse_mode='html')
    elif message.text == "📋 ИНСТРУКЦИЯ 📋":
        bot.send_message(message.chat.id, 'инструкция', parse_mode='html')
    elif message.text == "⚡ START ⚡":
        bot.send_message(message.chat.id, '/start', parse_mode='html')
    elif message.text == "🧑‍🎓 ОБУЧЕНИЕ 👩‍🎓":
        show_library(message)
    elif message.text == "🔄 RESTART 🔄":
        start(message)


bot.polling(none_stop=True, interval=0)
