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
    sql = "INSERT INTO dm_local (CIDADE, BAIRRO, ESTADO) VALUES (%s, %s, %s)"
    cursor.execute(sql, (city, district, state))
    database_connection.commit()
    cursor.close()

def insert_mobile(brand, title, state):
    cursor = database_connection.cursor()
    sql = "INSERT INTO dm_celular (MARCA, MODELO, ESTADO) VALUES (%s, %s, %s)"
    cursor.execute(sql, (brand, title, state ))
    database_connection.commit()
    cursor.close()

def insert_advertiser(name):
    cursor = database_connection.cursor()
    sql = "INSERT INTO dm_anunciante (NOME) VALUES (%s)"
    cursor.execute(sql, (name, ))
    database_connection.commit()
    cursor.close()

def insert_date(hour, day, moth, year="2022"):
    cursor = database_connection.cursor()
    sql = "INSERT INTO dm_tempo (HORA, DIA, MES, ANO) VALUES (%s, %s, %s, %s)"
    cursor.execute(sql, (hour, day, moth, year))
    database_connection.commit()
    cursor.close()

def close_db_connection():
    database_connection.close()
