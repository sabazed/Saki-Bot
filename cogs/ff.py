import discord
import random
import requests

from bs4 import BeautifulSoup
from discord.ext import commands

class Fun(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Loaded cog: {__name__[5:]}')

    @commands.command(aliases=['funfact'])
    async def ff(self, ctx):
        source = requests.get('http://randomfactgenerator.net').text
        soup = BeautifulSoup(source, 'lxml')
        await ctx.send(soup.find('div', id='z').text[:-6])

    @ff.error
    async def ff_error(self, ctx, error):
        await ctx.send('Unable to generate a fact.')

def setup(client):
    client.add_cog(Fun(client))