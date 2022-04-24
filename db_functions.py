import sqlite3


def insert_bot_users(user_id, tg_user_id, user_first_name, user_last_name, username, first_start_bot_date):
	try:
		connection = sqlite3.connect('db/test_bot.db')
		cur = connection.cursor()
		print("Подключен к SQLite")

		sqlite_insert_with_param = '''INSERT INTO bot_users
								(user_id, tg_user_id, user_first_name, user_last_name, username, first_start_bot_date)
								VALUES (?, ?, ?, ?, ?, ?)'''
		data_tuple = (user_id, tg_user_id, user_first_name, user_last_name, username, first_start_bot_date)
		cur.execute(sqlite_insert_with_param, data_tuple)
		print("данные внесны в bot_users")

		connection.commit()
		print("выполнен commit")
		cur.close()
		print("курсор закрыт")

	except sqlite3.Error as error:
		print("Ошибка при подключении к sqlite:", error)
	finally:
		if connection:
			connection.close()
			print("Соединение с SQLite остановлено")

def insert_bot_users_connections(connection_id, user_id, tg_user_id, connection_date):
	try:
		connection = sqlite3.connect('db/test_bot.db')
		cur = connection.cursor()
		print("Подключен к SQLite")

		sqlite_insert_with_param = '''INSERT INTO bot_users_connections
											(connection_id, user_id, tg_user_id, connection_date)
											VALUES (?, ?, ?, ?)'''
		data_tuple = (connection_id, user_id, tg_user_id, connection_date)
		cur.execute(sqlite_insert_with_param, data_tuple)
		print("данные внесны в bot_users_connections")

		connection.commit()
		print("выполнен commit")
		cur.close()
		print("курсор закрыт")

	except sqlite3.Error as error:
		print("Ошибка при подключении к sqlite:", error)
	finally:
		if connection:
			connection.close()
			print("Соединение с SQLite остановлено")

def count_bot_users():
	# проверка наличия строк в таблице
	# возвращает количество строк
	try:
		connection = sqlite3.connect('db/test_bot.db')
		cur = connection.cursor()
		print("Подключен к SQLite")

		sqlite_select = '''select count(*) from bot_users'''
		cur.execute(sqlite_select)
		records = cur.fetchone()
		print("количество строк посчитано и получено")

		connection.commit()
		print("выполнен commit")
		cur.close()
		print("курсор закрыт")

		return int(records[0])

	except sqlite3.Error as error:
		print("Ошибка при подключении к sqlite:", error)
	finally:
		if connection:
			connection.close()
			print("Соединение с SQLite остановлено")

def count_bot_users_connections():
	# проверка наличия строк в таблице
	# возвращает количество строк
	try:
		connection = sqlite3.connect('db/test_bot.db')
		cur = connection.cursor()
		print("Подключен к SQLite")

		sqlite_select = '''select count(*) from bot_users_connections'''
		cur.execute(sqlite_select)

		records = cur.fetchone()
		print("количество строк посчитано и получено")

		connection.commit()
		print("выполнен commit")
		cur.close()
		print("курсор закрыт")

		return int(records[0])

	except sqlite3.Error as error:
		print("Ошибка при подключении к sqlite:", error)
	finally:
		if connection:
			connection.close()
			print("Соединение с SQLite остановлено")

def max_id_value_bot_users():
	# получение наибольшего user_id из таблицы
	try:
		connection = sqlite3.connect('db/test_bot.db')
		cur = connection.cursor()
		print("Подключен к SQLite")

		sqlite_select = '''select max(user_id) from bot_users'''
		cur.execute(sqlite_select)
		records = cur.fetchone()
		print("максимальное значение bot_users.user_id получено")

		connection.commit()
		print("выполнен commit")
		cur.close()
		print("курсор закрыт")

		return int(records[0])

	except sqlite3.Error as error:
		print("Ошибка при подключении к sqlite:", error)
	finally:
		if connection:
			connection.close()
			print("Соединение с SQLite остановлено")

def max_id_value_bot_users_connections():
	# получение наибольшего user_id из таблицы
	try:
		connection = sqlite3.connect('db/test_bot.db')
		cur = connection.cursor()
		print("Подключен к SQLite")

		sqlite_select = '''select max(connection_id) from bot_users_connections'''
		cur.execute(sqlite_select)
		records = cur.fetchone()
		print("максимальное значение bot_users_connections.user_id получено")

		connection.commit()
		print("выполнен commit")
		cur.close()
		print("курсор закрыт")

		return int(records[0])

	except sqlite3.Error as error:
		print("Ошибка при подключении к sqlite:", error)
	finally:
		if connection:
			connection.close()
			print("Соединение с SQLite остановлено")

def unique_user_check(user_id):
	# проверка уникальности пользователя
	# возвращает True, если пользователь уникальный
	try:
		connection = sqlite3.connect('db/test_bot.db')
		cur = connection.cursor()
		print("Подключен к SQLite")

		us_id = int(user_id)
		sqlite_select = '''select count(*) from bot_users where tg_user_id = ?'''
		cur.execute(sqlite_select, (us_id,))

		count_of_users = cur.fetchone()
		value = int(count_of_users[0])

		connection.commit()
		print("выполнен commit")
		cur.close()
		print("курсор закрыт")

		if value == 0:
			print("Новый пользователь")
			return True
		else:
			print("Известный пользователь")
			return False

	except sqlite3.Error as error:
		print("Ошибка при подключении к sqlite:", error)
	finally:
		if connection:
			connection.close()
			print("Соединение с SQLite остановлено")

def get_user_id(tg_user_id):

	try:
		connection = sqlite3.connect('db/test_bot.db')
		cur = connection.cursor()
		print("Подключен к SQLite")

		tg_us_id = int(tg_user_id)
		sqlite_select = '''select user_id from bot_users where tg_user_id = ?'''
		cur.execute(sqlite_select, (tg_us_id,))
		us_id = cur.fetchone()
		print("user_id получен")

		connection.commit()
		print("выполнен commit")
		cur.close()
		print("курсор закрыт")

		return int(us_id[0])

	except sqlite3.Error as error:
		print("Ошибка при подключении к sqlite:", error)
	finally:
		if connection:
			connection.close()
			print("Соединение с SQLite остановлено")

def check_code(code):
	try:
		connection = sqlite3.connect('db/test_bot.db')
		cur = connection.cursor()
		print("Подключен к SQLite")

		sqlite_select = '''select region_name from regions_code where code_id = ?'''
		cur.execute(sqlite_select, (code,))
		region_name = cur.fetchone()
		print("данные по региону получены")

		connection.commit()
		print("выполнен commit")
		cur.close()
		print("курсор закрыт")

		return region_name

	except sqlite3.Error as error:
		print("Ошибка при подключении к sqlite:", error)
	finally:
		if connection:
			connection.close()
			print("Соединение с SQLite остановлено")
