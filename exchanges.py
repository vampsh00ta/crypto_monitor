
import requests
import json
import asyncio


async def read(file):
    f = open(file, 'r')
    params = json.load(f)

    f.close()
    return params


async def write(params ,file):
    f = open(file, 'w')
    f.write(json.dumps(params))
    f.close
class Exchanges:
    def __init__(self,token):
        self.token  = token.upper()
    async def binance(self):
        try:
            value = requests.get(f"https://api.binance.com/api/v3/depth?symbol={self.token}USDT&limit=1000").text
            return json.loads(value)['bids'][0][0]
        except:
            return 'error'

    async def coinlist(self):

        value = requests.get(f"https://trade-api.coinlist.co/v1/symbols/summary").text
        try:
            return  json.loads(value)[f'{self.token}-USD']['last_price']
        except:
            return  'error'

    async def coinbase(self):

        try:
            value = requests.get(f"https://api.coinbase.com/v2/exchange-rates?currency={self.token}").text
            return json.loads(value)['data']['rates']['USD']
        except:
            return 'error'

    async def ftx(self):

        try:
            value = requests.get(f"https://ftx.com/api/markets/{self.token}/USD").text
            return json.loads(value)['result']['price']
        except:
            return 'error'