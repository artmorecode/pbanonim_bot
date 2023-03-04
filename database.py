import sqlite3

class Database:
	def __init__(self, database_file):
		self.connection = sqlite3.connect(database_file, check_same_thread = False)
		self.cursor = self.connection.cursor()

	def add_user(self, name, chat_id):
		with self.connection:
			return self.cursor.execute('INSERT INTO `users` (`name`, `chat_id`, `roles`) VALUES (?,?,0)', (name, chat_id,))

	def add_queue(self, chat_id):
		with self.connection:
			return self.cursor.execute('INSERT INTO `queue` (`chat_id`) VALUES (?)', (chat_id,))

	def delete_queue(self, chat_id):
		with self.connection:
			return self.cursor.execute('DELETE FROM `queue` WHERE `chat_id` = (?)', (chat_id,))

	def delete_chat(self, id_chat):
		with self.connection:
			return self.cursor.execute('DELETE FROM `chats` WHERE `id` = ?', (id_chat,))

	def get_chat(self):
		with self.connection:
			chat = self.cursor.execute('SELECT * FROM `queue`', ()).fetchmany(1)

			if(bool(len(chat))):
				for row in chat:
					return row[1]
			else:
				return False

	def create_chat(self, chat_one, chat_two):
		with self.connection:
			if chat_two != 0:
				self.cursor.execute('DELETE FROM `queue` WHERE `chat_id` = (?)', (chat_two,))
				self.cursor.execute('INSERT INTO `chats` (`chat_one`, `chat_two`) VALUES (?,?)',(chat_one, chat_two,))
				return True

			else:
				return False

	def get_active_chat(self, chat_id):
		with self.connection:
			chat = self.cursor.execute('SELECT * FROM `chats` WHERE `chat_one` = ?', (chat_id,))

			id_chat = 0
			for row in chat:
				id_chat = row[0]
				chat_info = [row[0], row[2]]

			if id_chat == 0:
				chat = self.cursor.execute('SELECT * FROM `chats` WHERE `chat_two` = ?', (chat_id,))
				for row in chat:
					id_chat = row[0]
					chat_info = [row[0], row[1]]
				if id_chat == 0:
					return False
				else:
					return chat_info
			else:
				return chat_info

	def users(self):
		with self.connection:
			users = self.cursor.execute('SELECT * FROM `users`')

			for row in users:
				users = row[1]
				
				return users

	def spam(self):
		with self.connection:
			users = self.cursor.execute('SELECT * FROM `users`')

			for row in users:
				users = row[2]
				
				return users			

	def check_users(self, chat_id):
		with self.connection:
			return self.cursor.execute('SELECT `chat_id` FROM `users`').fetchmany(1)
			
	# def shop(self):
	# 	with self.connection:
	# 		return self.cursor.execute('SELECT * FROM `shop`')

	# def admin(self, chat_id):
	# 	with self.connection:
	# 		# users = self.cursor.execute('SELECT * FROM `users`')
	# 		self.cursor.execute('INSERT INTO `users` (`id`,`roles`) VALUES (3)', (chat_id,))

	# def add_product(self):
	# 	with self.connection:
	# 		product = self.cursor.execute('INSERT INTO `shop` (`name`, `price`)')