import math

from telebot import types
import globals
import database

from database import update_library_page, get_library_page


# rewrite if possible
def refresh_page(message):
    on_library_page = get_library_page(message.chat.id)
    if on_library_page is None:
        update_library_page(message.chat.id, 0)
        on_library_page = get_library_page(message.chat.id)
    names_on_page = types.InlineKeyboardMarkup(row_width=1)
    try:
        for i in range(on_library_page * globals.figures_content,
                       globals.figures_content * (on_library_page + 1)):
            name = database.figures[i][0]
            button = types.InlineKeyboardButton(name, callback_data=name)
            names_on_page.add(button)
    except IndexError:
        pass
    names_on_page.row_width = 3
    if on_library_page != 0 and not on_last_page(message.chat.id):
        prev_page = types.InlineKeyboardButton('⬅', callback_data='prev_figure')
        menu = types.InlineKeyboardButton('Menu', callback_data='menu')
        next_page = types.InlineKeyboardButton('➡', callback_data='next_figure')
        names_on_page.add(prev_page, menu, next_page)
    elif on_library_page == 0:
        menu = types.InlineKeyboardButton('Menu', callback_data='menu')
        next_page = types.InlineKeyboardButton('➡', callback_data='next_figure')
        names_on_page.add(menu, next_page)
    elif on_last_page(message.chat.id):
        menu = types.InlineKeyboardButton('Menu', callback_data='menu')
        prev_page = types.InlineKeyboardButton('⬅', callback_data='prev_figure')
        names_on_page.add(prev_page, menu)
    else:
        menu = types.InlineKeyboardButton('Menu', callback_data='menu')
        return menu
    return names_on_page


def to_next_page(message):
    update_library_page(message.chat.id, get_library_page(message.chat.id) + 1)
    update_curr_page(message)


def to_prev_page(message):
    update_library_page(message.chat.id, get_library_page(message.chat.id) - 1)
    update_curr_page(message)


def on_last_page(chat_id):
    on_library_page = get_library_page(chat_id)
    if on_library_page == 0 and database.number_of_definitions <= globals.definitions_content:
        return True
    elif (math.ceil(database.number_of_definitions / globals.definitions_content) - 1) == on_library_page:
        return True
    else:
        return False


def get_definition_in_form(name):
    return '🔸 ' + name + '\n\n📖 ' + database.get_figure_description(name) + '\n\n🌐 Development Corporation ®'


# outputs the page of definitions library
def show_definition_library(message):
    print_curr_page(message)


def delete_previous_library(chat_id):
    try:
        globals.bot.delete_message(chat_id=chat_id,
                                   message_id=database.get_last_library_id(chat_id))
    except Exception:
        pass


def print_curr_page(message):
    delete_previous_library(message.chat.id)
    last_library_message = globals.bot.send_message(chat_id=message.chat.id, text=globals.figures_library_title,
                                                    reply_markup=refresh_page(message))
    database.update_last_library_id(message.chat.id, last_library_message.message_id)


def update_curr_page(message):
    globals.bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id,
                                  text=globals.figures_library_title, reply_markup=refresh_page(message))
