import json
import requests
import discord
from discord.ext import commands
from datetime import  datetime
from discord_webhook import DiscordWebhook, DiscordEmbed
import asyncio
from funcs import binance,coinlist,coinbase,ftx,write,read


async def webhook(params,prices):
    webhook = DiscordWebhook(url='https://discord.com/api/webhooks/822921773732986900/uBOoVXlsdNYYO_sjfYa7tGQ4WFzHW75m4RpVBQbYDlBqlwSLCUc6T4CI1Ad_u6zSNtJJ')
    embed = DiscordEmbed()
    embed.set_author(
        name=f"{params['token']}",
        icon_url='https://cdn.discordapp.com/attachments/749196142310457368/916023328161026128/3p7mNEEQ7qQ.jpg'

    )
    embed.set_color(0xeb3434)
    
    embed.add_embed_field(name='Binance', value=f"{params['binance']} ->{abs((((float(prices['binance']) / float(params['binance'])) - 1) * 100)):.3f} -> {prices['binance']}", inline=False)
    embed.add_embed_field(name='Coinlist', value=f"{params['coinlist']} ->{abs((((float(prices['coinlist']) / float(params['coinlist'])) - 1) * 100)):.3f} -> {prices['coinlist']}", inline=False)
    embed.add_embed_field(name='Coinbase', value=f"{params['coinbase']} ->{abs((((float(prices['coinbase']) / float(params['coinbase'])) - 1) * 100)):.3f} -> {prices['coinbase']}", inline=False)
    embed.add_embed_field(name='Ftx', value=f"{params['ftx']} ->{abs((((float(prices['ftx']) / float(params['ftx'])) - 1) * 100)):.3f} -> {prices['ftx']}", inline=False)


        



    embed.set_footer(text=f'Made by *+oPiUM^)!^ * {datetime.time(datetime.now())}')
    webhook.add_embed(embed)
    webhook.execute()



async def percentage():
    execute = False
    params = await read("params.json")
    token = params['token']
    perc = params['percentage']
    if token != '' and perc != 0.0:
        prices_now = {
            'binance': await binance(token),
            'coinbase':await coinbase(token),
            'coinlist':await coinlist(token),
            'ftx':await ftx(token),
        }
        if perc > 0.0:
            try:
              
                
                if perc <((float(prices_now["binance"])/float(params["binance"]) )- 1)*100:
                    execute = True
                elif perc < ((float(prices_now["coinbase"])/float(params["coinbase"])) - 1)*100:
                    execute = True
                elif perc < ((float(prices_now["coinlist"])/float(params["coinlist"])) - 1)*100:
                    execute = True
                elif perc < ((float(prices_now["ftx"])/float(params["ftx"]) - 1))*100:
                    execute = True
            except:
                execute = True
        else:

            try:
                if -perc < (float((params["binance"]))/float(prices_now["binance"]) - 1)*100:
                    execute = True
                elif -perc < (float((params["coinbase"]))/float(prices_now["coinbase"]) - 1)*100:
                    execute = True
                elif -perc < (float((params["coinlist"]))/float(prices_now["coinlist"]) - 1)*100:
                    execute = True
                elif -perc < (float((params["ftx"]))/float(prices_now["ftx"]) - 1)*100:
                    execute = True
            except:
                execute = True
        if execute:
    
            await  webhook(params,prices_now)
    
            params['token'] = ''
            params['percentage'] = 0.0
            await write(params, "monitoring params.json")
            print("execute")
            print(prices_now["binance"], prices_now["coinlist"], prices_now["coinbase"], prices_now["ftx"])
    
        else:
            print(prices_now["binance"], prices_now["coinlist"], prices_now["coinbase"], prices_now["ftx"])
            await asyncio.sleep(0.1)
            await percentage()
    