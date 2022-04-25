import db_functions
import constants
import ui_functions
import datetime
import logic_functions

my_bot = constants.Bot()
bot = my_bot.bot


@bot.message_handler(commands=['start'])
def start_message(message):
    tg_us_id = message.from_user.id
    us_first_name = message.from_user.first_name
    us_last_name = message.from_user.last_name
    us_name = message.from_user.username
    log_in_date = datetime.datetime.now()

    bot.send_message(message.from_user.id,
                     "Привет, %s!\n\n"
                     "Я - бот, который поможет узнать название региона по его коду c авто номера.\n\n"
                     "Выберите действие:" % us_first_name,
                     reply_markup=ui_functions.create_buttons())

    print(tg_us_id, us_first_name, us_last_name, us_name, log_in_date)

    logic_functions.db_users_check(tg_us_id, us_first_name, us_last_name, us_name, log_in_date)


@bot.message_handler(content_types='text')
def search_code(message):
    if message.text != 'Ввести код региона:':
        bot.send_message(message.from_user.id,
                         "Прежде чем отправить код региона,\n"
                         "нажмите на кнопку 'Ввести код региона' ----> [: :]")
    elif message.text == 'Ввести код региона:':
        bot.register_next_step_handler(message, get_code)


def get_code(message):
    get_value = db_functions.check_code(message.text)

    if get_value:
        info = ("%s\n\nЕсли хотите узнать еще один регион, "
                "нажмите на кнопку \n'Ввести код региона' "
                "повторно и введите код" % str(get_value[0]))
        bot.send_message(message.from_user.id, info)
    else:
        bot.send_message(message.from_user.id,
                         "Вы ввели несуществующий код.\n\nЕсли хотите узнать регион, "
                         "нажмите на кнопку\nВвести код региона' повторно и введите код")

    # elif message.text == 'Вывести весь список':


bot.infinity_polling()
