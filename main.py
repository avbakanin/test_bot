import db_functions
import telebot
from telebot import types
import datetime

token = '5230208511:AAFmQuWhnXt2VVfg8zyqfIw37rK5AzRlTFU'
bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def start_message(message):
    tg_us_id = message.from_user.id
    us_first_name = message.from_user.first_name
    us_last_name = message.from_user.last_name
    us_name = message.from_user.username
    log_in_date = datetime.datetime.now()

    reply_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    enter_button = types.KeyboardButton("Ввести код региона:")
    info_button = types.KeyboardButton("Вывести весь список")

    # inline_markup = types.InlineKeyboardMarkup(row_width=1)
    # inline_button = types.InlineKeyboardButton("Inline button", url="https://yandex.ru/")

    reply_markup.row(enter_button, info_button)
    # inline_markup.add(inline_button)

    bot.send_message(message.from_user.id, "Привет, " + us_first_name +
                            '!\n\n'
                            + "Я - бот, который поможет узнать название региона "
                              "по его коду c авто номера.\n"
                              "\n"
                              "Выберите действие:",
                            reply_markup=reply_markup)

    print(tg_us_id, us_first_name, us_last_name, us_name, log_in_date)

    def db_users_check(tg_us_id, us_first_name, us_last_name, usname, log_in_date):
        count_users = db_functions.count_bot_users()

        if count_users == 0:
            print("Самый первый уникальный пользователь")
            db_functions.insert_bot_users(1, tg_us_id, us_first_name, us_last_name, usname, log_in_date)
            db_functions.insert_bot_users_connections(1, 1, tg_us_id, log_in_date)
        elif db_functions.unique_user_check(tg_us_id):
            # новый уникальный пользователь
            bot_users_max_id = db_functions.max_id_value_bot_users()
            bot_users_connections_max_id = db_functions.max_id_value_bot_users_connections()
            print(str(bot_users_max_id + 1) + " уникальных пользователей(я)")
            # уникальный пользователь сначала добавляется в таблицу пользователей
            db_functions.insert_bot_users(bot_users_max_id + 1,
                                tg_us_id,
                                us_first_name,
                                us_last_name,
                                usname,
                                log_in_date)
            # затем уникальный пользователь добавляется в таблицу коннектов
            db_functions.insert_bot_users_connections(bot_users_connections_max_id + 1,
                                            bot_users_max_id + 1,
                                            tg_us_id,
                                            log_in_date)
        else:
            # неуникальный пользователь
            # информация добавляется только в таблицу с коннектами
            bot_users_connections_max_id = db_functions.max_id_value_bot_users_connections()
            user_id = db_functions.get_user_id(tg_us_id)
            db_functions.insert_bot_users_connections(bot_users_connections_max_id + 1, user_id, tg_us_id, log_in_date)

    db_users_check(tg_us_id, us_first_name, us_last_name, us_name, log_in_date)


@bot.message_handler(content_types='text')
def search_code(message):
    if message.text != 'Ввести код региона:':
        bot.send_message(message.from_user.id,
                         "Прежде чем отправить код региона \n"
                         "нажмите на кнопку 'Ввести код региона' ----> [: :]")
    elif message.text == 'Ввести код региона:':
        bot.register_next_step_handler(message, get_code)

def get_code(message):
    get_value = db_functions.check_code(message.text)

    if get_value:
        info = (str(get_value[0]) + "\n \nЕсли хотите узнать еще один регион, "
                                    "нажмите на кнопку \n'Ввести код региона' повторно "
                                    "и введите код")
        bot.send_message(message.from_user.id, info)
    else:
         bot.send_message(message.from_user.id, "Вы ввели несуществующий код" +
                             "\n \nЕсли хотите узнать регион, "
                             "нажмите на кнопку \n'Ввести код региона' повторно "
                             "и введите код")

    # elif message.text == 'Вывести весь список':


bot.infinity_polling()
