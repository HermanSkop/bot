import pathlib

from telebot import types

import figures_library
import globals
import definitions_library
from database import *

bot = globals.bot


# outputs main menu
@bot.callback_query_handler(func=lambda call: check_menu(call.data))
def return_to_menu(call):
    if call.data == 'menu':
        # bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        # next line should be changed to something else
        start(call.message)
    elif call.data == 'prev_def':
        definitions_library.to_prev_page(call.message)
    elif call.data == 'next_def':
        definitions_library.to_next_page(call.message)
    elif call.data == 'prev_figure':
        figures_library.to_prev_page(call.message)
    elif call.data == 'next_figure':
        figures_library.to_next_page(call.message)
    bot.answer_callback_query(call.id, text='menu')


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
                        message_text=definitions_library.get_definition_in_form(name[0])))
            )
            id += 1
    for name in figures:
        print(name[0])
        print(get_image_of_figure(name[0]))
        if query.query.lower() in name[0].lower():
            results.append(
                types.InlineQueryResultArticle(id=str(id), title=name[0], description=name[1],
                                               input_message_content=types.InputTextMessageContent(
                                                   message_text=figures_library.get_definition_in_form(name[0])))
            )
            id += 1
    bot.answer_inline_query(query.id, results, cache_time=1)


# check_name checks if the given name in names of definitions
def check_definition(name):
    for definition in definitions:
        if definition[0] == name:
            return True
    return False


@bot.callback_query_handler(func=lambda call: check_definition(call.data))
def show_definition(call):
    bot.send_message(call.message.chat.id, definitions_library.get_definition_in_form(call.data))
    bot.answer_callback_query(call.id, text=call.data)


# check_name checks if the given name in names of figures
def check_figure(name):
    for figure in figures:
        if figure[0] == name:
            return True
    return False


@bot.callback_query_handler(func=lambda call: check_figure(call.data))
def show_figure_definition(call):
    try:
        bot.send_photo(chat_id=call.message.chat.id, photo=open(get_image_of_figure(call.data), 'rb'),
                       caption=figures_library.get_definition_in_form(call.data))
    except FileNotFoundError:
        bot.send_message(chat_id=call.message.chat.id, text=figures_library.get_definition_in_form(call.data))
    bot.answer_callback_query(call.id, text=call.data)


# check_menu checks if the given text is menu or left/right button
def check_menu(text):
    if text == 'menu' or text == 'prev_def' or text == 'next_def' or text == 'prev_figure' or text == 'next_figure':
        return True
    else:
        return False


@bot.message_handler(commands=["start"])
def start(message):
    update_library_page(message.chat.id, 0)
    definitions_library.delete_previous_library(message.chat.id)
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
        definitions_library.show_definition_library(message)
    elif message.text == "📕 ОБУЧЕНИЕ 📗":
        figures_library.show_definition_library(message)
    elif message.text == "🔄 RESTART 🔄":
        start(message)


bot.polling(none_stop=True, interval=0)
