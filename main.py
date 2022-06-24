import json
import requests
import discord
from discord.ext import commands
from datetime import datetime
from discord_webhook import DiscordWebhook, DiscordEmbed
from exchanges import Exchanges, write, read
from monitor import Monitor


async def webhook(token):
    webhook = DiscordWebhook(
        url='https://discord.com/api/webhooks/822921773732986900/uBOoVXlsdNYYO_sjfYa7tGQ4WFzHW75m4RpVBQbYDlBqlwSLCUc6T4CI1Ad_u6zSNtJJ')
    embed = DiscordEmbed()
    embed.set_author(
        name=f"Exchanges",
        icon_url='https://cdn.discordapp.com/attachments/749196142310457368/916023328161026128/3p7mNEEQ7qQ.jpg'

    )
    reqs = Exchanges(token)

    embed.set_color(0xeb3434)
    embed.add_embed_field(name='Token Name', value=token.upper(), inline=False)
    embed.add_embed_field(name='Binance', value=await reqs.binance(), inline=True)
    embed.add_embed_field(name='Coinlist', value=await reqs.coinlist(), inline=True)
    embed.add_embed_field(name='Coinbase', value=await reqs.coinbase(), inline=True)
    embed.add_embed_field(name='FTX', value=str(await reqs.ftx()), inline=True)

    embed.set_footer(text=f'Made by *+oPiUM^)!^ * {datetime.time(datetime.now())}')
    webhook.add_embed(embed)
    webhook.execute()


bot = commands.Bot(command_prefix=('!'))


@bot.command()
async def perc(ctx):
    message = ctx.message.content.split(' ')
    embed = discord.Embed(title="Began monitoring", color=0xeb3434)

    if len(message) == 3:
        token = message[1]
        reqs = Exchanges(token)

        params = {
            "percentage": float(message[2]),
            "token": message[1],
            "binance": await reqs.binance(),
            "coinlist": await reqs.coinlist(),
            "coinbase": await reqs.coinbase(),
            "ftx": await reqs.ftx()
        }

        embed.add_field(name='Token', value=params['token'], inline=True)
        if params['percentage'] > 0:
            embed.add_field(name='Percent', value=f"↑{params['percentage']}", inline=True)
        else:
            embed.add_field(name='Percent', value=f"↓{-params['percentage']}", inline=True)
        await ctx.send(embed=embed)

        await write(params, "params.json")
        print(params)
    else:
        params = {
            "percentage": 0.0,
            "token": "",
            "binance": 0.0,
            "coinlist": 0.0,
            "coinbase": 0.0,
            "ftx": 0.0
        }
        await write(params, "params.json")
        print(params)
    await monitor.percMonitor()


@bot.command()
async def c(ctx):
    token = ctx.message.content.split(' ')[1]

    await webhook(token)


@bot.command()
async def sp(ctx):
    message = ctx.message.content.split(' ')
    embed = discord.Embed(title="Began monitoring", color=0xeb3434)
    params = {
        "token": message[1].upper(),
        "price": float(message[2])
    }
    print(message)

    embed.add_field(name='Token', value=params['token'], inline=True)
    if params['price'] > 0:
        embed.add_field(name='Price Point', value=f">{params['price']}", inline=True)
    else:
        embed.add_field(name='Price Point', value=f"<{-params['price']}", inline=True)
    await ctx.send(embed=embed)

    await write(params, "monitoring params.json")
    await monitor.ordMonitor()

monitor = Monitor()
bot.run('OTg5OTM5ODc4MTEwMzIyNjg5.GYyU9E.fQR2lYGAm6VnvSW-nPHe0YOBP25Fc7Td7nEUAg')