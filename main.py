import math
import re
import sqlite3

import cursor as cursor
import telebot
from _sqlite3 import Error
from aiogram import types
from telebot import types

bot = telebot.TeleBot('')

last_library_message = None

page = 0
content = 5

pattern = re.compile(r'\w', re.MULTILINE)


@bot.inline_handler(func=lambda query: len(query.query) > 0)
def show_list(query):
    try:
        matches = re.match(pattern, query.query)
        # Вылавливаем ошибку, если вдруг юзер ввёл чушь
        # или задумался после ввода первого числа
    except AttributeError as ex:
        return
    results = []
    id = 0
    for name in definitions:
        if name[0] == query.query:
            results.append(
                types.InlineQueryResultArticle(
                    id=str(id), title=name[0],
                    description=name[1],
                    input_message_content=types.InputTextMessageContent(message_text="works"))
            )
            id += 1
    bot.answer_inline_query(query.id, results, cache_time=1)


def on_last_page():
    if page == 0 and number_of_definitions <= content:
        return True
    elif (math.ceil(number_of_definitions / content) - 1) == page:
        return True
    else:
        return False


# check_name checks if the given name in names of definitions`
def check_name(name):
    for definition in definitions:
        if definition[0] == name:
            return True
    return False


# returns description of the definition
def get_description(name):
    for definition in definitions:
        if definition[0] == name:
            return definition[1]
    return 'No description yet('


@bot.callback_query_handler(func=lambda call: check_name(call.data))
def show_definition(call):
    message = '🔸 ' + call.data + '\n\n📖 ' + get_description(call.data) + '\n\n🌐 Development Corporation ™'
    bot.send_message(call.message.chat.id, message)
    bot.answer_callback_query(call.id, text=call.data)


# check_menu checks if the given text is menu or left/right button
def check_menu(text):
    if text == 'menu' or text == 'prev' or text == 'next':
        return True
    else:
        return False


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


@bot.message_handler(commands=["start"])
def start(message):
    send_mess = f'Здравствуйте, {message.from_user.first_name} {message.from_user.last_name}!\n' \
                f'Да начнётся ваше изучение терминов из нашей библиотеки!\n' \
                f'/library - команда активирует режим поиска по библиотеке\n' \
                f'/help - команда вызывает список команд\n' \
                f'/start - Запускает бота\n' \
                f'На этом пока что всё, так что удачи в использовании нашего бота!'
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row_width = 2
    btn1 = types.KeyboardButton("📚 ТЕРМИНЫ 📚")
    btn2 = types.KeyboardButton("📈 ФИГУРЫ 📉")
    btn3 = types.KeyboardButton("🗞 НОВОСТИ 🗞")
    btn4 = types.KeyboardButton("⚡ START ⚡")

    markup.add(btn1, btn2, btn3, btn4)
    bot.send_message(message.chat.id, send_mess, reply_markup=markup)


# rewrite if possible
def refresh_page():
    global page
    name = 'ads'
    names_on_page = types.InlineKeyboardMarkup(row_width=1)
    for i in range(page * content, content * (page + 1)):
        name = definitions[i][0]
        button = types.InlineKeyboardButton(name, callback_data=name)
        names_on_page.add(button)
    names_on_page.row_width = 3
    if page != 0 and not on_last_page():
        prev_page = types.InlineKeyboardButton('⬅', callback_data='prev')
        menu = types.InlineKeyboardButton('Menu', callback_data='menu')
        next_page = types.InlineKeyboardButton('➡', callback_data='next')
        names_on_page.add(prev_page, menu, next_page)
    elif page == 0:
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


def print_curr_page(message):
    global last_library_message
    try:
        bot.delete_message(chat_id=last_library_message.chat.id, message_id=last_library_message.message_id)
    except Exception:
        print('No such chat exists')
    last_library_message = bot.send_message(chat_id=message.chat.id, text='Библиотека',
                                            reply_markup=refresh_page())


def update_curr_page(message):
    bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text='Библиотека',
                          reply_markup=refresh_page())


def to_next_page(message):
    global page
    page += 1
    update_curr_page(message)


def to_prev_page(message):
    global page
    page -= 1
    update_curr_page(message)


# outputs the whole library
@bot.message_handler(commands=["library"])
def libsearch(message):
    print_curr_page(message)


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
        btn3 = types.KeyboardButton("📋 ИНСТРУКЦИЯ 📋")
        btn4 = types.KeyboardButton("🔄 RESTART 🔄")

        markup.add(btn1, btn2, btn3, btn4)
        bot.send_message(message.chat.id, 'Выберите действие', reply_markup=markup)
    elif message.text == "📈 ФИГУРЫ 📉":
        bot.send_message(message.chat.id, 'фигуры', parse_mode='html')
    elif message.text == "🗞 НОВОСТИ 🗞":
        bot.send_message(message.chat.id, 'новости', parse_mode='html')
    elif message.text == "🧑‍💻 ПРОВЕРЬ СЕБЯ 👩‍💻":
        bot.send_message(message.chat.id, 'Выберите действие', parse_mode='html')
    elif message.text == "📋 ИНСТРУКЦИЯ 📋":
        bot.send_message(message.chat.id, 'инструкция', parse_mode='html')
    elif message.text == "⚡ START ⚡":
        bot.send_message(message.chat.id, '/start', parse_mode='html')
    elif message.text == "🧑‍🎓 ОБУЧЕНИЕ 👩‍🎓":
        libsearch(message)
    elif message.text == "🔄 RESTART 🔄":
        start(message)


def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection


def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")


def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")


connection = create_connection('db.sqlite')

create_definitions_table = """
CREATE TABLE IF NOT EXISTS definitions (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  description TEXT
);
"""

create_defs = """
INSERT INTO
  definitions (name, description)
VALUES
  ('Ферма', 'множественное оборудование для майнинга криптовалют, объединенных в одну сеть'),
  ('Тело свечи', 'термин, демонстрирующий промежуток между ценами открытия и закрытия временного периода'),
  ('Тень свечи', 'показатель минимального и максимального курса криптовалюты во временном промежутке'),
  ('Сатоши Накамото', 'псевдоним предполагаемого создателя первой в мире криптовалюты биткоин'),
  ('Разворот', 'состояние, когда настроение рынка меняется на противоположную сторону'),
  ('Газ', 'комиссия майнерам для выполнения транзакции в сети Эфире'),
  ('Вторичка', 'покупка NFT из вторых рук в меркетплейсе'),
  ('Листинг', 'выставление NFT на продажу в маркетплейсе'),
  ('Делистинг', 'снятие NFT с продажи'),
  ('Рар, рарность', 'степень редкости NFT в коллекции. Чем реже NFT, тем она дороже'),
  ('Минт', 'покупка NFT на сайте создателей коллекции'),
  ('Вайт лист', 'список человек, имеющих право на минт NFT в числе первых'),
  ('Паблик сейл', 'открытие продаж для всех желающих'),
  ('Ревил', 'открытие вашего NFT. Почти все коллекции скрыты, чтобы избежать массового слива в первые дни листинга'),
  ('холд', 'хранение NFT в долгосрок');
"""

# Created_table = execute_read_query(connection, create_definitions_table)
Inserted_values = execute_read_query(connection, create_defs)

select_definitions = 'SELECT name, description from definitions'
select_number_of_definitions = 'SELECT COUNT(name) from definitions'

definitions = execute_read_query(connection, select_definitions)
number_of_definitions = execute_read_query(connection, select_number_of_definitions)[0][0]
delete_comment = "DELETE FROM definitions WHERE id = 1"

bot.polling(none_stop=True, interval=0)
