import db_functions
import constants
import datetime

my_bot = constants.BotConstants()
bot = my_bot.bot
db = db_functions.DbConnectedFuncs()


def log_user_connection_from_start(user_info):
    if db.count_bot_users() == 0:
        print("Самый первый уникальный пользователь")
        db.insert_bot_users(1,
                            user_info['tg_id'],
                            user_info['name'],
                            user_info['surname'],
                            user_info['username'],
                            user_info['log_in_date'])
        db.insert_bot_users_connections(1, 1,  user_info['tg_id'], user_info['log_in_date'])
    elif db.is_new_user(user_info['tg_id']):
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
                            user_info['log_in_date'])
        # затем уникальный пользователь добавляется в таблицу коннектов
        db.insert_bot_users_connections(bot_users_connections_max_id + 1,
                                        bot_users_max_id + 1,
                                        user_info['tg_id'],
                                        user_info['log_in_date'])
    else:
        # неуникальный пользователь
        # информация добавляется только в таблицу с коннектами
        bot_users_connections_max_id = db.max_id_value_bot_users_connections()
        user_db_info = db.get_user_db_info(user_info['tg_id'])
        # print(list(user_db_info)[2:5])
        db.insert_bot_users_connections(bot_users_connections_max_id + 1,
                                        user_db_info[0],
                                        user_info['tg_id'],
                                        user_info['log_in_date'])
        # должны проверить изменились ли данные пользователя
        db.update_bot_users(user_info)


def get_user_info(message):
    log_in_date = datetime.datetime.now()

    user_info = {'tg_id': message.from_user.id,
                 'name': message.from_user.first_name,
                 'surname': message.from_user.last_name,
                 'username': message.from_user.username,
                 'log_in_date': log_in_date}

    print(user_info['name'],
          user_info['surname'],
          user_info['username'],
          user_info['log_in_date'])

    return user_info


def search_code(message):
    get_value = db.get_info_by_code_region(message.text)
    if get_value:
        info = (str(get_value[0]))
        bot.send_message(message.from_user.id, info)
        print("данные по региону %s получены" % message.text)
    elif message.text == 'Вывести весь список':
        text_message = db.get_all_list()
        text = str()
        for i in range(0, 138):
            i_text = text_message[i][0] + ': \t\t\t' + text_message[i][1]
            text = text + i_text + '\n'
        bot.send_message(message.from_user.id, text)
    else:
        bot.send_message(message.from_user.id,
                         "Вы ввели несуществующий код."
                         "\nВведите код заново")
        print('введен несуществующий код')


def log_user_connection_from_text(user_info):
    bot_users_connections_max_id = db.max_id_value_bot_users_connections()
    user_db_info = db.get_user_db_info(user_info['tg_id'])
    db.insert_bot_users_connections(bot_users_connections_max_id + 1,
                                    user_db_info[0],
                                    user_info['tg_id'],
                                    user_info['log_in_date'])
    db.update_bot_users(user_info)
