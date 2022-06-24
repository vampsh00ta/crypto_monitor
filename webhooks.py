from discord_webhook import DiscordWebhook, DiscordEmbed
from datetime import datetime
class Webhooks:
    async def percWebhook(self,params, prices):
        webhook = DiscordWebhook(
            url='https://discord.com/api/webhooks/822921773732986900/uBOoVXlsdNYYO_sjfYa7tGQ4WFzHW75m4RpVBQbYDlBqlwSLCUc6T4CI1Ad_u6zSNtJJ')
        embed = DiscordEmbed()
        embed.set_author(
            name=f"{params['token']}",
            icon_url='https://cdn.discordapp.com/attachments/749196142310457368/916023328161026128/3p7mNEEQ7qQ.jpg'

        )
        embed.set_color(0xeb3434)

        embed.add_embed_field(name='Binance',
                              value=f"{params['binance']} ->{abs((((float(prices['binance']) / float(params['binance'])) - 1) * 100)):.3f} -> {prices['binance']}",
                              inline=False)
        embed.add_embed_field(name='Coinlist',
                              value=f"{params['coinlist']} ->{abs((((float(prices['coinlist']) / float(params['coinlist'])) - 1) * 100)):.3f} -> {prices['coinlist']}",
                              inline=False)
        embed.add_embed_field(name='Coinbase',
                              value=f"{params['coinbase']} ->{abs((((float(prices['coinbase']) / float(params['coinbase'])) - 1) * 100)):.3f} -> {prices['coinbase']}",
                              inline=False)
        embed.add_embed_field(name='Ftx',
                              value=f"{params['ftx']} ->{abs((((float(prices['ftx']) / float(params['ftx'])) - 1) * 100)):.3f} -> {prices['ftx']}",
                              inline=False)

        embed.set_footer(text=f'Made by *+oPiUM^)!^ * {datetime.time(datetime.now())}')
        webhook.add_embed(embed)
        webhook.execute()

    async def ordWebhook(self,params, prices):
        webhook = DiscordWebhook(
            url='https://discord.com/api/webhooks/822921773732986900/uBOoVXlsdNYYO_sjfYa7tGQ4WFzHW75m4RpVBQbYDlBqlwSLCUc6T4CI1Ad_u6zSNtJJ')
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