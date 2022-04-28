import logic_functions
import ui_functions


@logic_functions.bot.message_handler(commands=['start'])
def start_message(message):
    user_info = logic_functions.get_user_info(message)
    logic_functions.log_user_connection_from_start(user_info)
    logic_functions.bot.send_message(message.from_user.id,
                                     "Привет, %s!\n\n"
                                     "Для того чтобы узнать название федеральной территориальной единицы, "
                                     "введите ее код:" % message.from_user.first_name,
                                     reply_markup=ui_functions.create_buttons())


@logic_functions.bot.message_handler(content_types='text')
def text_message(message):
    user_info = logic_functions.get_user_info(message)
    logic_functions.log_user_connection_from_text(user_info)
    logic_functions.search_code(message)


logic_functions.bot.infinity_polling()
