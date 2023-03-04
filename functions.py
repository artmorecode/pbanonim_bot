import sqlite3
import telebot
import config
from config import db, token

def admin_message(text):
    return db.spam()
# def stats():
#     conn = db
#     cursor = conn.cursor()
#     row = cursor.execute(f'SELECT user_id FROM users').fetchone()
#     amount_user_all = 0
#     while row is not None:
#         amount_user_all += 1
#         row = cursor.fetchone()
#     msg = ' Информация:\n\n Пользователей в боте - ' + str(amount_user_all)
#     return msg
#     conn.close()