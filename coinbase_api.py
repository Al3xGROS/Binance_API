import requests
import json
import sqlite3

# LIST OF ALL AVAILABLE CRYPTOCURRENCIES
def getAllCrypto():
    uri = 'https://api.pro.coinbase.com/currencies'
    response = requests.get(uri).json()

    for i in range(len(response)):
        if response[i]['details']['type'] == 'crypto':
            print(response[i]['id'])


# FUNCTION TO DISPLAY THE 'ASK' OR 'BID' PRICE OF AN ASSET
def getDepth(direction, pair):
    url = "https://api.exchange.coinbase.com/products/" + pair + "/book?level=1"
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers)
    dic = json.loads(response.text)

    if direction == "bids":
        print(dic.get("bids"))
    else:
        print(dic.get("asks"))


# GET ORDER BOOK FOR AN ASSET
def getOrderBook(asset):
    url = "https://api.exchange.coinbase.com/products/" + asset + "/book?level=2"
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers)

    print(response.text)


# FUNCTION TO READ CANDLES (FOR A DURATION OF 5 MINUTES => DURATION = 300)
def refreshDataCandle(pair, duration):
    url = "https://api.exchange.coinbase.com/products/" + pair + "/candles?granularity=" + str(duration)
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers)
    print(response.text)


# SQLITE TABLE 
def connectTable():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS dataCandles
                (Id INTEGER PRIMARY KEY, date INT, high REAL, low REAL, open REAL, close REAL, volume REAL)''')

    connection.commit()
    connection.close()

connectTable()