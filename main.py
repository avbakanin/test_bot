import db_functions
import logic_functions


@logic_functions.bot.message_handler(commands=['start'])
def start_message(message):
    logic_functions.start_message(message)


@logic_functions.bot.message_handler(content_types='text')
def search_code(message):
    if message.text != 'Ввести код региона:':
        logic_functions.bot.send_message(message.from_user.id,
                         "Прежде чем отправить код региона,\n"
                         "нажмите на кнопку 'Ввести код региона' ----> [: :]")
    elif message.text == 'Ввести код региона:':
        logic_functions.bot.register_next_step_handler(message, get_code)


def get_code(message):
    get_value = db_functions.check_code(message.text)

    if get_value:
        info = ("%s\n\nЕсли хотите узнать еще один регион, "
                "нажмите на кнопку \n'Ввести код региона' "
                "повторно и введите код" % str(get_value[0]))
        logic_functions.bot.send_message(message.from_user.id, info)
    else:
        logic_functions.bot.send_message(message.from_user.id,
                         "Вы ввели несуществующий код.\n\nЕсли хотите узнать регион, "
                         "нажмите на кнопку\nВвести код региона' повторно и введите код")

    # elif message.text == 'Вывести весь список':


logic_functions.bot.infinity_polling()
