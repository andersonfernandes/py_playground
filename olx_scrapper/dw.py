import mysql.connector

database_connection = mysql.connector.connect(
    host='localhost',
    user='root',
    password='root',
    database='olx_database'
)

def insert_place(city, district, state='Alagoas'):
    cursor = database_connection.cursor()
    sql = "INSERT IGNORE INTO DM_LOCAL (CIDADE, BAIRRO, ESTADO) VALUES (%s, %s, %s)"
    cursor.execute(sql, (city, district, state))
    database_connection.commit()
    cursor.close()

def close_db_connection():
    database_connection.close()
