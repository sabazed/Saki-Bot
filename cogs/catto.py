import discord
import requests

from discord.ext import commands

class Fun(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Loaded cog: {__name__[5:]}')

    @commands.command(aliases=['cat', 'neko'])
    async def catto(self, ctx):

        content = requests.get('http://aws.random.cat/meow').text
        url = content[9:-2].replace('\\','')
            
        embed = discord.Embed(title='Meow')
        embed.set_image(url=url)

        await ctx.send(embed=embed)
        
    @catto.error
    async def caterror(self, ctx, error):
        await ctx.send('Can\'t generate a cat picture.')

def setup(client):
    client.add_cog(Fun(client))
