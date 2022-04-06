import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

database_connection = mysql.connector.connect(
    host='localhost',
    user=os.getenv('DATABASE_USER'),
    password=os.getenv('DATABASE_PASSWORD'),
    database=os.getenv('DATABASE_NAME')
)

def insert_place(city, district, state='Alagoas'):
    cursor = database_connection.cursor()
    sql = "REPLACE INTO dm_local (CIDADE, BAIRRO, ESTADO) VALUES (%s, %s, %s)"
    cursor.execute(sql, (city, district, state))
    database_connection.commit()
    cursor.close()

def close_db_connection():
    database_connection.close()
