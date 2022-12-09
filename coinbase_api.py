import requests
import json

# GET A LIST OF ALL AVAILABLE CRYPTOCURRENCIES AND DISPLAY IT
def getAllCrypto():
    uri = 'https://api.pro.coinbase.com/currencies'
    response = requests.get(uri).json()

    for i in range(len(response)):
        if response[i]['details']['type'] == 'crypto':
            print(response[i]['id'])


# CREATE A FUNCTION TO DISPLAY THE 'ASK' OR 'BID' PRICE OF AN ASSET
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

getOrderBook("BTC-USD")