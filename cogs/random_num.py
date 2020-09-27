import discord
import random

from discord.ext import commands

class Fun(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Loaded cog: {__name__[5:]}')


    @commands.command(aliases=['random'])  # RANDOM NUMBER
    async def random_num(self, ctx, start=0, end=1):
        maxn = int(max(start, end))
        minn = int(min(start, end))
        await ctx.send(str(random.randint(minn, maxn)))

    @random_num.error
    async def rndnumerr(self, ctx, error):
        await ctx.send('You should specify two valid numbers.')

def setup(client):
    client.add_cog(Fun(client))