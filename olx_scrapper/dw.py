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

def insert_TPM_ETL(brand, title, condition, price, name, hour, day, moth, city, district, state="Alagoas", year="2022"):
    cursor = database_connection.cursor()
    sql = "INSERT INTO tmp_etl (MARCA, MODELO, CONDICAO, PRECO, NOME, HORA, DIA, MES, CIDADE, BAIRRO, ESTADO, ANO ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    cursor.execute(sql, (brand, title, condition, price, name, hour, day, moth, city, district, state, year))
    database_connection.commit()
    cursor.close()

def insert_place():
    cursor = database_connection.cursor()
    sql = "INSERT INTO dm_local SELECT DISTINCT null, ESTADO, CIDADE, BAIRRO  FROM olx_database.tmp_etl"
    cursor.execute(sql)
    database_connection.commit()
    cursor.close()

def insert_mobile():
    cursor = database_connection.cursor()
    sql = "INSERT INTO dm_celular SELECT DISTINCT null, MARCA, MODELO, CONDICAO FROM olx_database.tmp_etl"
    cursor.execute(sql)
    database_connection.commit()
    cursor.close()

def insert_advertiser():
    cursor = database_connection.cursor()
    sql = "INSERT INTO dm_anunciante SELECT DISTINCT null, NOME FROM olx_database.tmp_etl"
    cursor.execute(sql)
    database_connection.commit()
    cursor.close()

def insert_date():
    cursor = database_connection.cursor()
    sql = "INSERT INTO dm_tempo SELECT DISTINCT null, ANO, MES, DIA, HORA FROM olx_database.tmp_etl"
    cursor.execute(sql)
    database_connection.commit()
    cursor.close()

def insert_fact_ads():
    cursor = database_connection.cursor()
    sql = "INSERT INTO dm_fato_anuncios SELECT c.ID_CELULAR, t.ID_TEMPO, l.ID_LOCAL, a.ID_ANUNCIANTE, x.PRECO FROM olx_database.tmp_etl x, olx_database.dm_local  l, olx_database.dm_celular c, olx_database.dm_anunciante a, olx_database.dm_tempo t WHERE x.ESTADO = l.ESTADO AND x.CIDADE = l.CIDADE AND x.BAIRRO = l.BAIRRO AND x.MARCA = c.MARCA AND x.MODELO = c.MODELO AND x.CONDICAO = c.CONDICAO AND x.NOME = a.NOME AND x.ANO = t.ANO AND x.MES = t.MES AND x.DIA = t.DIA AND x.HORA = t.HORA"
    cursor.execute(sql)
    database_connection.commit()
    cursor.close()

def close_db_connection():
    database_connection.close()
