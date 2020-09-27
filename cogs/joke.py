import discord
import joke_generator
# import random
# import requests

# from bs4 import BeautifulSoup
from discord.ext import commands

class Fun(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Loaded cog: {__name__[5:]}')

    @commands.command()
    async def joke(self, ctx):
        await ctx.send(joke_generator.generate())

    # @commands.command(aliases=['jk'])
    # async def joke(self, ctx):
    #     source = requests.get('https://generatorfun.com/joke-generator').text
    #     soup = BeautifulSoup(source, 'lxml')
    #     embed = discord.Embed(title = soup.find('div', id='gencount').h2.text[:-6],
    #                           description = soup.find('div', id='gencount').p.text)

    @joke.error
    async def jokeerror(self, ctx, error):
        await ctx.send('Unable to generate a joke.')

def setup(client):
    client.add_cog(Fun(client))