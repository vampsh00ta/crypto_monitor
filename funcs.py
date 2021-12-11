import requests
import json
import asyncio


async def read(file):
    f = open(file, 'r')
    params = json.load(f)

    f.close()
    return params


async def write(params,file):
    f = open(file, 'w')
    f.write(json.dumps(params))
    f.close
    
async def binance(token):
    token = token.upper()
    try:
        value = requests.get(f"https://api.binance.com/api/v3/depth?symbol={token}USDT&limit=1000").text
        return json.loads(value)['bids'][0][0]
    except:
        return 'error'

async def coinlist(token):
    token = token.upper()
    value = requests.get(f"https://trade-api.coinlist.co/v1/symbols/summary").text
    try:
        return  json.loads(value)[f'{token}-USD']['last_price']
    except:
        return  'error'
    
async def coinbase(token):
    token = token.upper()
    try:
        value = requests.get(f"https://api.coinbase.com/v2/exchange-rates?currency={token}").text
        return json.loads(value)['data']['rates']['USD']
    except:
        return 'error'
    
async def ftx(token):
    token = token.upper()
    try:
        value = requests.get(f"https://ftx.com/api/markets/{token}/USD").text
        return json.loads(value)['result']['price']
    except:
        return 'error'
