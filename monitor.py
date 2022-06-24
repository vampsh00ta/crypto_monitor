import requests
import json
from datetime import datetime
from discord_webhook import DiscordWebhook, DiscordEmbed
import asyncio
import websocket
from webhooks import Webhooks
from exchanges import Exchanges, write, read


class Monitor(Webhooks):


    async def ordMonitor(self):
        execute = False

        params = await read("monitoring params.json")
        token = params['token']
        price = params['price']

        if token != '' and price != 0.0:
            reqs = Exchanges(token)

            prices = {
                "binance": await reqs.binance(),
                "coinlist": await reqs.coinbase(),
                "coinbase": await reqs.coinlist(),
                "ftx": await reqs.ftx()
            }

            if params['price'] > 0:
                try:
                    if price < float(prices["binance"]):
                        execute = True
                    elif price < float(prices["coinlist"]):
                        execute = True
                    elif price < float(prices["coinbase"]):
                        execute = True
                    elif price < float(prices["ftx"]):
                        execute = True
                except:
                    execute = True
            else:
                try:
                    if -price > float(prices["binance"]):
                        execute = True
                    elif -price > float(prices["coinlist"]):
                        execute = True
                    elif -price > float(prices["coinbase"]):
                        execute = True
                    elif -price > float(prices["ftx"]):
                        execute = True
                except:
                    execute = True
            print(prices["binance"], prices["coinlist"], prices["coinbase"], prices["ftx"])
            if execute:

                await self.ordMonitor(params, prices)
                params['token'] = ''
                params['price'] = 0.0
                print("execute")
                await write(params, "monitoring params.json")

            else:
                await asyncio.sleep(0.1)
                await self.ordMonitor()
    async def percMonitor(self):
        execute = False
        params = await read("params.json")
        token = params['token']
        perc = params['percentage']
        if token != '' and perc != 0.0:
            reqs = Exchanges(token)

            prices_now  = {
                "binance": await reqs.binance(),
                "coinlist": await reqs.coinbase(),
                "coinbase": await reqs.coinlist(),
                "ftx": await reqs.ftx()
            }
            if perc > 0.0:
                try:

                    if perc < ((float(prices_now["binance"]) / float(params["binance"])) - 1) * 100:
                        execute = True
                    elif perc < ((float(prices_now["coinbase"]) / float(params["coinbase"])) - 1) * 100:
                        execute = True
                    elif perc < ((float(prices_now["coinlist"]) / float(params["coinlist"])) - 1) * 100:
                        execute = True
                    elif perc < ((float(prices_now["ftx"]) / float(params["ftx"]) - 1)) * 100:
                        execute = True
                except:
                    execute = True
            else:

                try:
                    if -perc < (float((params["binance"])) / float(prices_now["binance"]) - 1) * 100:
                        execute = True
                    elif -perc < (float((params["coinbase"])) / float(prices_now["coinbase"]) - 1) * 100:
                        execute = True
                    elif -perc < (float((params["coinlist"])) / float(prices_now["coinlist"]) - 1) * 100:
                        execute = True
                    elif -perc < (float((params["ftx"])) / float(prices_now["ftx"]) - 1) * 100:
                        execute = True
                except:
                    execute = True
            if execute:

                await  self.percWebhook(params, prices_now)

                params['token'] = ''
                params['percentage'] = 0.0
                await write(params, "monitoring params.json")
                print("execute")
                print(prices_now["binance"], prices_now["coinlist"], prices_now["coinbase"], prices_now["ftx"])

            else:
                print(prices_now["binance"], prices_now["coinlist"], prices_now["coinbase"], prices_now["ftx"])
                await asyncio.sleep(0.1)
                await self.percMonitor()
