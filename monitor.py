import requests
import json
from datetime import  datetime
from discord_webhook import DiscordWebhook, DiscordEmbed
import asyncio
import websocket

from funcs import binance,coinlist,coinbase,ftx,write,read



async def webhook(params,prices):
    webhook = DiscordWebhook(url='https://discord.com/api/webhooks/822921773732986900/uBOoVXlsdNYYO_sjfYa7tGQ4WFzHW75m4RpVBQbYDlBqlwSLCUc6T4CI1Ad_u6zSNtJJ')
    embed = DiscordEmbed()

    if params['price'] > 0:
        embed.set_author(
            name=f"{params['token'].upper()} above {params['price']}",
            icon_url='https://cdn.discordapp.com/attachments/749196142310457368/916023328161026128/3p7mNEEQ7qQ.jpg'

        )
    else:
        embed.set_author(
            name=f"{params['token'].upper()} under {-params['price']}",
            icon_url='https://cdn.discordapp.com/attachments/749196142310457368/916023328161026128/3p7mNEEQ7qQ.jpg'

        )

    embed.set_color(0xeb3434)
    embed.add_embed_field(name='Binance', value=prices["binance"], inline=True)
    embed.add_embed_field(name='Coinlist', value=prices["coinlist"], inline=True)
    embed.add_embed_field(name='Coinbase', value=prices["coinbase"], inline=True)
    embed.add_embed_field(name='Coinbase', value=str(prices["ftx"]), inline=True)
    embed.set_footer(text=f'Made by *+oPiUM^)!^ * {datetime.time(datetime.now())}')
    webhook.add_embed(embed)
    webhook.execute()


async def monitor():

    execute = False
    
    params = await read("monitoring params.json")
    token = params['token']
    price = params['price']
    
    
    if token != '' and price != 0.0:
        prices = {
            "binance":await binance(token),
            "coinlist":await coinbase(token),
            "coinbase":await coinlist(token),
            "ftx":await ftx(token)
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
    
            await webhook(params,prices)
            params['token'] = ''
            params['price'] = 0.0
            print("execute")
            await write(params,"monitoring params.json")
    
        else:
            await asyncio.sleep(0.1)
            await monitor()





