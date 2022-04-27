import sqlite3

class Db_connected_funcs():

	def start_connection(self, db):
		'подключение к бд'
		connection = sqlite3.connect(db, check_same_thread=False)
		cur = connection.cursor()
		connect_info = {'connect': connection, 'cur': cur}

		return connect_info

	def stop_connection(self, connection, cur):
		'отключение от бд'
		connection.commit()
		cur.close()
		connection.close()
		print("выполнен commit, курсор закрыт, соединение с SQLite остановлено")

	def count_bot_users(self):
		'''проверка наличия строк в таблице
		возвращает количество строк'''
		try:
			started_connection = self.start_connection('db/test_bot.db')
			connection = started_connection.get('connect')
			cur = started_connection.get('cur')

			sqlite_select = '''select count(*) from bot_users'''
			cur.execute(sqlite_select)
			data_records = cur.fetchone()
			print("Подключен к SQLite\n"
				  "количество строк посчитано и получено: %s" % str(data_records[0]))

			self.stop_connection(connection, cur)

			return int(data_records[0])

		except sqlite3.Error as error:
			print("-------------> Ошибка при подключении к sqlite", error)

	def insert_bot_users(self, user_id, tg_user_id, user_first_name, user_last_name, username, first_start_bot_date):
		'вставляет строку в таблицу bot_users'
		started_connection = self.start_connection('db/test_bot.db')
		connection = started_connection.get('connect')
		cur = started_connection.get('cur')

		sqlite_insert_with_param = '''INSERT INTO bot_users
									(user_id, tg_user_id, user_first_name, user_last_name, username, first_start_bot_date)
									VALUES (?, ?, ?, ?, ?, ?)'''
		data_tuple = (user_id, tg_user_id, user_first_name, user_last_name, username, first_start_bot_date)
		cur.execute(sqlite_insert_with_param, data_tuple)
		print("данные внесны в таблицу bot_users")

		self.stop_connection(connection, cur)

	def insert_bot_users_connections(self, connection_id, user_id, tg_user_id, connection_date):
		'вставляет строку в таблицу bot_users_connections'
		started_connection = self.start_connection('db/test_bot.db')
		connection = started_connection.get('connect')
		cur = started_connection.get('cur')

		sqlite_insert_with_param = '''INSERT INTO bot_users_connections
											(connection_id, user_id, tg_user_id, connection_date)
											VALUES (?, ?, ?, ?)'''
		data_tuple = (connection_id, user_id, tg_user_id, connection_date)
		cur.execute(sqlite_insert_with_param, data_tuple)
		print("данные внесены в таблицу bot_users_connections")

		self.stop_connection(connection, cur)

	def unique_user_check(self, user_id):
		'''проверка уникальности пользователя
		возвращает True, если пользователь уникальный'''
		started_connection = self.start_connection('db/test_bot.db')
		connection = started_connection.get('connect')
		cur = started_connection.get('cur')

		us_id = int(user_id)
		sqlite_select = '''select count(*) from bot_users where tg_user_id = ?'''
		cur.execute(sqlite_select, (us_id,))

		count_of_users = cur.fetchone()
		value = int(count_of_users[0])

		self.stop_connection(connection, cur)

		if value == 0:
			print("Новый пользователь")
			return True
		else:
			print("Известный пользователь")
			return False

	def max_id_value_bot_users(self):
		'получение наибольшего user_id из таблицы bot_users'
		started_connection = self.start_connection('db/test_bot.db')
		connection = started_connection.get('connect')
		cur = started_connection.get('cur')

		sqlite_select = '''select max(user_id) from bot_users'''
		cur.execute(sqlite_select)
		records = cur.fetchone()
		print("максимальное значение bot_users.user_id получено: %s" % str(records[0]))

		self.stop_connection(connection, cur)

		return int(records[0])

	def max_id_value_bot_users_connections(self):
		'получение наибольшего user_id из таблицы bot_users_connections'
		started_connection = self.start_connection('db/test_bot.db')
		connection = started_connection.get('connect')
		cur = started_connection.get('cur')

		sqlite_select = '''select max(connection_id) from bot_users_connections'''
		cur.execute(sqlite_select)
		records = cur.fetchone()
		print("максимальное значение bot_users_connections.user_id получено: %s" %str(records[0]))

		self.stop_connection(connection, cur)

		return int(records[0])

	def get_user_db_info(self, tg_user_id):
		'получить bot_users.user_id по значению tg_user_id'
		started_connection = self.start_connection('db/test_bot.db')
		connection = started_connection.get('connect')
		cur = started_connection.get('cur')

		tg_us_id = int(tg_user_id)
		sqlite_select = '''select * from bot_users where tg_user_id = ?'''
		cur.execute(sqlite_select, (tg_us_id,))
		us_info = cur.fetchone()
		print("bot_users.user_id получен: %s" %str(us_info[0]))

		self.stop_connection(connection, cur)

		return us_info

	def update_bot_users(self, user_info):
		'обновить данные пользователя'
		started_connection = self.start_connection('db/test_bot.db')
		connection = started_connection.get('connect')
		cur = started_connection.get('cur')

		user_info = list(user_info.values())
		sql_update_query = '''update bot_users
							  set user_first_name = ?, user_last_name = ?, username = ?
							  where tg_user_id = ?'''
		data_tuple = (user_info[1], user_info[2], user_info[3], user_info[0])
		cur.execute(sql_update_query, data_tuple)
		print("данные в таблицe bot_users у пользователя %s обновлены" % user_info[0] )

		self.stop_connection(connection, cur)


def check_code(code):
	try:
		connection = sqlite3.connect('db/test_bot.db')
		cur = connection.cursor()

		sqlite_select = '''select region_name from regions_code where code_id = ?'''
		cur.execute(sqlite_select, (code,))
		print("Подключен к SQLite")

		region_name = cur.fetchone()
		print("данные по региону %s получены" % str(code))

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

def count_bot_users_connections():
	# проверка наличия строк в таблице
	# возвращает количество строк
	try:
		connection = sqlite3.connect('db/test_bot.db')
		cur = connection.cursor()

		sqlite_select = '''select count(*) from bot_users_connections'''
		cur.execute(sqlite_select)
		print("Подключен к SQLite")

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


