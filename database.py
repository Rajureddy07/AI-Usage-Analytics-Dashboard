import psycopg2


connection = psycopg2.connect(

    host="localhost",
    database="ai_data_usage",
    user="postgres",
    password="123raju"
)

cursor = connection.cursor()

cursor.execute("SELECT * FROM usage_data")

rows = cursor.fetchall()

for row in rows:
    print(row)

cursor.close()
connection.close()