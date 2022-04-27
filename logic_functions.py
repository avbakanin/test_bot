import db_functions
import constants
import datetime
import ui_functions
import collections

my_bot = constants.Bot()
bot = my_bot.bot
db = db_functions.Db_connected_funcs()


def identity_check(user_info, user_db_info):
    user_info = list(user_info.values())[1:]
    user_db_info = list(user_db_info)[2:5]
    if collections.Counter(user_info) == collections.Counter(user_db_info):
        return True


def db_users_check(user_info, log_in_date):
    if db.count_bot_users() == 0:
        print("Самый первый уникальный пользователь")
        db.insert_bot_users(1,
                            user_info['tg_id'],
                            user_info['name'],
                            user_info['surname'],
                            user_info['username'], log_in_date)
        db.insert_bot_users_connections(1, 1,  user_info['tg_id'], log_in_date)
    elif db.unique_user_check(user_info['tg_id']):
        # новый уникальный пользователь
        bot_users_max_id = db.max_id_value_bot_users()
        bot_users_connections_max_id = db.max_id_value_bot_users_connections()
        print(str(bot_users_max_id + 1) + " уникальных пользователей(я)")
        # уникальный пользователь сначала добавляется в таблицу пользователей
        db.insert_bot_users(bot_users_max_id + 1,
                            user_info['tg_id'],
                            user_info['name'],
                            user_info['surname'],
                            user_info['username'],
                            log_in_date)
        # затем уникальный пользователь добавляется в таблицу коннектов
        db.insert_bot_users_connections(bot_users_connections_max_id + 1,
                                        bot_users_max_id + 1,
                                        user_info['tg_id'],
                                        log_in_date)
    else:
        # неуникальный пользователь
        # информация добавляется только в таблицу с коннектами
        bot_users_connections_max_id = db.max_id_value_bot_users_connections()
        user_db_info = db.get_user_db_info(user_info['tg_id'])
        # print(list(user_db_info)[2:5])
        db.insert_bot_users_connections(bot_users_connections_max_id + 1,
                                        user_db_info[0],
                                        user_info['tg_id'],
                                        log_in_date)
        # должны проверить изменились ли данные пользователя
        if not identity_check(user_info, user_db_info):
            db.update_bot_users(user_info)


def start_message(message):
    log_in_date = datetime.datetime.now()

    user_info = {'tg_id': message.from_user.id,
                 'name': message.from_user.first_name,
                 'surname': message.from_user.last_name,
                 'username': message.from_user.username}

    bot.send_message(message.from_user.id,
                     "Привет, %s!\n\n"
                     "Я - бот, который поможет узнать название региона по его коду c авто номера.\n\n"
                     "Выберите действие:" % user_info['name'],
                     reply_markup=ui_functions.create_buttons())

    print(user_info['tg_id'],
          user_info['name'],
          user_info['surname'],
          user_info['username'], log_in_date)
    # print(list(user_info.values())[1:])

    db_users_check(user_info, log_in_date)
