import json
import sqlite3

connection = sqlite3.connect('chat_bot.db')
cursor = connection.cursor()

cursor.execute("SELECT * FROM Users")

table = cursor.fetchall()
head = [
    'user_id',
    'username',
    'date',
    'name',
    'depart_city',
    'resort',
    'quan',
    'dates',
    'nights',
    'budget',
    'messanger',
    'number'
]
table_dict = []
k = 0
for i in table:
    dictionary = dict(zip(head, table[k]))
    table_dict.append(dictionary)
    k += 1
with open('users.json', mode='w', buffering=-1, encoding='utf-8') as f:
    json.dump(table, f, indent=2)
