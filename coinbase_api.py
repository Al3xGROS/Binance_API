import requests
import json
import sqlite3
import ast

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


# SQLITE TABLE TO STORE DATA FROM FUNCTION ABOVE 
def storeData(data, table):
    # Connect to the database
    conn = sqlite3.connect("test.db")

    # Create a cursor object
    cursor = conn.cursor()

    # Create the table (if it doesn't already exist)
    if table == "dataCandles":    
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS dataCandles(id INTEGER PRIMARY KEY, date INTEGER, high REAL, low REAL, open REAL, close REAL, volume REAL)"
        )

        # The list of data
        newData = ast.literal_eval(data)

        # Insert the data into the table
        for row in newData:
            cursor.execute(
                "INSERT INTO dataCandles(date, open, high, low, close, volume) VALUES (?, ?, ?, ?, ?, ?)",
                row,
            )
    elif table == "fullDataSet":
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS fullDataSet(id INTEGER PRIMARY KEY, uuid TEXT, traded_crypto REAL, price REAL, created_at_int INT, side TEXT)"
        )

        # The list of data
        # newData = ast.literal_eval(data)

        # Insert the data into the table
        for record in data:
            cursor.execute(
                "INSERT INTO fullDataSet(uuid, traded_crypto, price, created_at_int, side) VALUES (?, ?, ?, ?, ?)",
                (record['trade_id'], record['size'], record['price'], record['time'], record['side']),
            )

    # Commit the transaction
    conn.commit()

    # Close the connection
    conn.close()


# FUNCTION TO READ CANDLES (PAIR FORMAT EXAMPLE : "BTC-USD" ; FOR A DURATION OF 5 MINUTES => DURATION = 300)
def refreshDataCandle(pair, duration):
    url = "https://api.exchange.coinbase.com/products/" + pair + "/candles?granularity=" + str(duration)
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers)
    # print(response.text)
    storeData(response.text, "dataCandles")


# MODIFY REFRESHDATACANDLE() TO UPDATE WHEN NEW CANDLE DATA IS AVAILABLE
# def refreshDataCandle2(pair, duration):
#     url = "https://api.exchange.coinbase.com/products/" + pair + "/candles?granularity=" + str(duration)
#     headers = {"accept": "application/json"}
#     response = requests.get(url, headers=headers)
#     storeDataCandle(response.text)


# FUNCTION TO EXTRACT ALL AVAILABLE TRADE DATA
def refreshData(pair):
    url = "https://api.exchange.coinbase.com/products/" + pair + "/trades"
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers)
    # print(response)
    # print(type(response))
    data = json.loads(response.text)
    storeData(data, "fullDataSet")

