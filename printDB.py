import sqlite3

connection = sqlite3.connect('data.db')

cursor = connection.cursor()


select_query = "SELECT * FROM users"
for row in cursor.execute(select_query):
    print(row)

select_query1 = "SELECT * FROM sensors"
for row in cursor.execute(select_query1):
    print(row)

connection.commit()
connection.close()