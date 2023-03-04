import config
import telebot
from telebot import types
from telebot.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from database import Database
from PyEasyQiwi import QiwiConnection
from time import sleep
import functions as func

api_key = "eyJ2ZXJzaW9uIjoiUDJQIiwiZGF0YSI6eyJwYXlpbl9tZXJjaGFudF9zaXRlX3VpZCI6IjJtOGxlai0wMCIsInVzZXJfaWQiOiI3OTA0NjgxODQxNCIsInNlY3JldCI6IjdkYjU1MmVkNWY1ZDkwZDMxZmY0NjBhZDJiNzE4YWI0MmQ2NTFmM2I4MDk3Mzg1MGQ0OGYwZjYyZmM3NThmMDUifX0="
conn = QiwiConnection(api_key)

db = Database('db.db')
bot = telebot.TeleBot(config.token)


@bot.message_handler(commands=['start'])
def start(message):
	if db.check_users(message.chat.id):
		markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
		# item0 = types.KeyboardButton('📑 Меню')
		item1 = types.KeyboardButton('🔍 Поиск собеседника')
		# item2 = types.KeyboardButton('🏪 Магазин')
		markup.add(item1)

		bot.send_message(message.chat.id, '👋🏻Свозращением, {0.first_name} {0.last_name}!👋🏻 \n🔍Нажми на поиск собеседника чтобы начать общение🔍'.format(message.from_user), reply_markup = markup)
	else:
		db.add_user(message.from_user.username, message.chat.id)

		markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
		# item0 = types.KeyboardButton('📑 Меню')
		item1 = types.KeyboardButton('🔍 Поиск собеседника')
		# item2 = types.KeyboardButton('🏪 Магазин')
		markup.add(item1)

		bot.send_message(message.chat.id, '👋🏻Привет, {0.first_name} {0.last_name}!👋🏻 \n🤖Добро пожаловать в анонимный чатик🤖 \n🔍Нажми на поиск собеседника чтобы начать общение🔍'.format(message.from_user), reply_markup = markup)

@bot.message_handler(commands=['menu'])
def menu(message):		
	markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
	item1 = types.KeyboardButton('🔍 Поиск собеседника')
	# item2 = types.KeyboardButton('🏪 Магазин')
	markup.add(item1)

	bot.send_message(message.chat.id, '📑 Меню'.format(message.from_user), reply_markup = markup)

@bot.message_handler(commands=['stop'])
def stop(message):
	chat_info = db.get_active_chat(message.chat.id)
	if chat_info != False:
		db.delete_chat(chat_info[0])
		markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
		item1 = types.KeyboardButton('🔍 Поиск собеседника')
		markup.add(item1)

		bot.send_message(chat_info[1], '❌ Собеседник вышел из чата', reply_markup = markup)
		bot.send_message(message.chat.id, '❌ Вы покинули чат', reply_markup = markup)
	else:
		bot.send_message(message.chat.id, '❗ Вы не начали чат')

@bot.message_handler(content_types=['text'])
def bot_message(message):
	if message.chat.type == 'private':
		if message.text == '🔍 Поиск собеседника':
			markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
			item1 = types.KeyboardButton('❌ Остановить поиск')
			markup.add(item1)

			chat_two = db.get_chat()

			if db.create_chat(message.chat.id, chat_two) == False:
				db.add_queue(message.chat.id)
				bot.send_message(message.chat.id, '👁‍🗨 Идёт поиск собеседника...', reply_markup = markup)
			else:
				msg = '💬Собеседник найден!\n🤖Советую спросить его имя🤖 \nЧтобы остановить диалог, нажми /stop'

				markups = types.ReplyKeyboardMarkup(resize_keyboard = True)
				item1 = types.KeyboardButton('/stop')
				markups.add(item1)

				bot.send_message(message.chat.id, msg, reply_markup = markups)
				bot.send_message(chat_two, msg, reply_markup = markups)

		elif message.text == '❌ Остановить поиск':

			markup1 = types.ReplyKeyboardMarkup(resize_keyboard = True)
			item2 = types.KeyboardButton('🔍 Поиск собеседника')
			markup1.add(item2)

			db.delete_queue(message.chat.id)
			bot.send_message(message.chat.id, '❗ Поиск собеседника остановлен', reply_markup = markup1)

		elif message.text == 'admin':
			if message.chat.id in config.adm_id:
				markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
				item1 = types.KeyboardButton('Список пользователей бота👨🏻‍💼')
				item2 = types.KeyboardButton('Рассылка💬')
				markup.add(item1, item2)

				msg = '🔱АДМИН МЕНЮ🔱'

				bot.send_message(message.chat.id, msg, reply_markup=markup)
			else:
				markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
				item1 = types.KeyboardButton('🔍 Поиск собеседника')
				markup.add(item1)
				bot.send_message(message.chat.id, '📛Тебе сюда нельзя📛', reply_markup=markup)

		elif message.text == 'Список пользователей бота👨🏻‍💼':
			if message.chat.id in config.adm_id:
				adm = config.adm_id
					
				markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
				item1 = types.KeyboardButton('Вернуться назад ⏪')
				markup.add(item1)

				users = db.users()
				bot.send_message(message.chat.id, f'Список пользователей: \n@{users}', reply_markup=markup)
			else:
				markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
				item1 = types.KeyboardButton('🔍 Поиск собеседника')
				markup.add(item1)
				bot.send_message(message.chat.id, '📛Тебе сюда нельзя📛', reply_markup=markup)

		elif message.text == 'Рассылка💬':
			if message.chat.id in config.adm_id:	
				markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
				item1 = types.KeyboardButton('Список пользователей бота👨🏻‍💼')
				item2 = types.KeyboardButton('Рассылка💬')
				markup.add(item1, item2)

				msg = bot.send_message(message.chat.id, 'Введите текст для рассылки. \n\nДля отмены напишите "-" без кавычек!', reply_markup=markup)
				bot.register_next_step_handler(msg, message1)
			else:
				markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
				item1 = types.KeyboardButton('🔍 Поиск собеседника')
				markup.add(item1)
				bot.send_message(message.chat.id, '📛Тебе сюда нельзя📛', reply_markup=markup)

		# elif message.text == 'Рассылка💬':
		# 	if message.chat.id in config.adm_id:
		# 		bot.send_message(message.chat.id, '💬Введите текст рассылки💬')
		# 		bot.register_next_step_handler(message, spam)
		# 	else:
		# 		markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
		# 		item1 = types.KeyboardButton('🔍 Поиск собеседника')
		# 		markup.add(item1)
		# 		bot.send_message(message.chat.id, '📛Тебе сюда нельзя📛', reply_markup=markup)

		elif message.text == 'Вернуться назад ⏪':
			if message.chat.id in config.adm_id:
				markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
				item1 = types.KeyboardButton('Список пользователей бота👨🏻‍💼')
				item2 = types.KeyboardButton('Рассылка💬')
				markup.add(item1, item2)

				msg = '🔱АДМИН МЕНЮ🔱'

				bot.send_message(message.chat.id, msg, reply_markup=markup)
			else:
				markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
				item1 = types.KeyboardButton('🔍 Поиск собеседника')
				markup.add(item1)
				bot.send_message(message.chat.id, '📛Тебе сюда нельзя📛', reply_markup=markup)

	else:
		chat_info = db.get_active_chat(message.chat.id)
		bot.send_message(chat_info[1], f'Собеседник: {message.text}')

def message1(message):
    text = message.text
    info = func.admin_message(text)
    bot.send_message(message.chat.id, 'Рассылка начата!')
    bot.send_message(info, text)
    bot.send_message(message.chat.id, 'Рассылка завершена!')

# def spam(message):
#     users = db.users()
#     txt = message.text
#     try:
#     	bot.send_message(users, txt)
    
#     # for z in range(len(users)):
#     #     try:
#     #     	txt = message.text
#     #         bot.send_message(users[z][0], txt)
#     #     except:
#     #         pass
#     bot.send_message(message.chat.id, 'Рассылка завершена')	

		# elif message.text == '🏪 Магазин':
		# 	markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
		# 	item0 = types.KeyboardButton('📑 Меню')
		# 	item1 = types.KeyboardButton('👑ADMIN👑')
		# 	item2 = types.KeyboardButton('👮MODER👮')
		# 	item3 = types.KeyboardButton('⚙️TESTER⚙️')
		# 	markup.add(item0, item1, item2, item3)

		# 	db.shop()
		# 	msg = '''

		# 	   NAME | PRICE

		# 	  ADMIN | 100₽
		# 	  MODER | 50₽
		# 	 TESTER | 150₽

		# 	'''
		# 	bot.send_message(message.chat.id, msg, reply_markup=markup)

		# elif message.text == '👑ADMIN👑':
		# 	markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
		# 	item0 = types.KeyboardButton('📑 Меню')
		# 	item4 = types.KeyboardButton('❇Провереть счёт')
		# 	markup.add(item0, item4)

		# 	pay_url, bill_id, response = conn.create_bill(value=1.00, description="admin")

		# 	bot.send_message(message.chat.id, pay_url, reply_markup=markup)

		# 	db.admin(message.chat.id)

		# elif message.text == '❇Провереть счёт':
		# 	pay_url, bill_id, response = conn.create_bill(value=1.00, description="admin")
		# 	status, response = conn.check_bill(bill_id)
		# 	if status == 'PAID':
		# 		bot.send_message(message.chat.id, '✅Счёт оплачен')
		# 		db.admin(message.chat.id)

		# 	else:
		# 		bot.send_message(message.chat.id, '❌Ты не оплатил')

		# elif message.text == '👮MODER👮':
		# 	pass

		# elif message.text == '⚙️TESTER⚙️':
		# 	pass

		# elif message.text == '📑 Меню':
		# 	markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
		# 	item1 = types.KeyboardButton('🔍 Поиск собеседника')
		# 	item2 = types.KeyboardButton('🏪 Магазин')
		# 	markup.add(item1, item2)

		# 	bot.send_message(message.chat.id, '📑 Меню'.format(message.from_user), reply_markup = markup)

		


bot.polling(none_stop=True)