import db_functions


def db_users_check(tg_us_id, us_first_name, us_last_name, us_name, log_in_date):
    db = db_functions.Db_connected_funcs()

    count_users = db.count_bot_users()

    if count_users == 0:
        print("Самый первый уникальный пользователь")
        db.insert_bot_users(1, tg_us_id, us_first_name, us_last_name, us_name, log_in_date)
        db.insert_bot_users_connections(1, 1, tg_us_id, log_in_date)
    elif db.unique_user_check(tg_us_id):
        # новый уникальный пользователь
        bot_users_max_id = db.max_id_value_bot_users()
        bot_users_connections_max_id = db.max_id_value_bot_users_connections()
        print(str(bot_users_max_id + 1) + " уникальных пользователей(я)")
        # уникальный пользователь сначала добавляется в таблицу пользователей
        db.insert_bot_users(bot_users_max_id + 1,
                            tg_us_id,
                            us_first_name,
                            us_last_name,
                            us_name,
                            log_in_date)
        # затем уникальный пользователь добавляется в таблицу коннектов
        db.insert_bot_users_connections(bot_users_connections_max_id + 1,
                                        bot_users_max_id + 1,
                                        tg_us_id,
                                        log_in_date)
    else:
        # неуникальный пользователь
        # информация добавляется только в таблицу с коннектами
        bot_users_connections_max_id = db.max_id_value_bot_users_connections()
        user_id = db.get_user_id(tg_us_id)
        db.insert_bot_users_connections(bot_users_connections_max_id + 1, user_id, tg_us_id, log_in_date)
