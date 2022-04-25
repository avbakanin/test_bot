from telebot import types

def create_buttons():
    reply_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    enter_button = types.KeyboardButton("Ввести код региона:")
    info_button = types.KeyboardButton("Вывести весь список")

    # inline_markup = types.InlineKeyboardMarkup(row_width=1)
    # inline_button = types.InlineKeyboardButton("Inline button", url="https://yandex.ru/")

    reply_markup.row(enter_button, info_button)
    # inline_markup.add(inline_button)

    return reply_markup