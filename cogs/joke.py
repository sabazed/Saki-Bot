import discord
import joke_generator

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

    @joke.error
    async def jokeerror(self, ctx, error):
        await ctx.send('Unable to generate a joke.')

def setup(client):
    client.add_cog(Fun(client))
