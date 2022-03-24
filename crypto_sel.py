import pandas as pd
import requests
import mysql.connector
import time

mydb = mysql.connector.connect(host="localhost",user="root",password="root",database="bdcriptomoeda")

r =requests.get('https://coingecko.com/')
df = pd.read_html(r.text)[0]
df["Coin"]=df["Coin"].apply(lambda x: x.split("  ")[0])
df["Price"]=df["Price"].apply(lambda x: x.replace(",","").replace("$",""))
df["1h"]=df["1h"].apply(lambda x: x.replace(",","").replace("%",""))
df["24h"]=df["24h"].apply(lambda x: x.replace(",","").replace("%",""))
df["24h Volume"]=df["24h Volume"].apply(lambda x: x.replace(",","").replace("$",""))
df["Mkt Cap"]=df["Mkt Cap"].apply(lambda x: x.replace(",","").replace("$",""))

mycursor = mydb.cursor()

i = 0
for x in df:
    sql = "INSERT INTO tblcotacaomoeda (nomMoeda,valPreco,valVariacao1Hora,valVariacao24Horas,valVolumeTransacao,valCapitalizacaoMerc) VALUES (" + "'" + df["Coin"][i] + "'," + df["Price"][i] + "," + df["1h"][i] + "," + df["24h"][i] + "," + df["24h Volume"][i] + "," + df["Mkt Cap"][i] + ")"
    mycursor.execute(sql)
    i=i+1
mydb.commit()
time.sleep(10)
