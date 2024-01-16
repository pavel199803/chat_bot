import json
import sqlite3

connection = sqlite3.connect('chat_bot.db')
cursor = connection.cursor()

cursor.execute("SELECT * FROM Users")

table = cursor.fetchall()
with open('users.json', mode='w', buffering=-1, encoding='utf-8') as f:
    json.dump(table, f, indent=2)