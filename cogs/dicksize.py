import discord
import random

from discord.ext import commands


class Fun(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Loaded cog: {__name__[5:]}')

    @commands.command(aliases=['dicksize', 'dick'])  # DICK SIZE
    async def dsize(self, ctx, member: discord.Member = None):
        size = random.randint(0, 20)
        if size > 14:
            dick = '**B' + size * '=' + 'D**'
        else:
            dick = 'B' + size * '=' + 'D'
        if member == None:
            member = ctx.message.author
        message = discord.Embed(
            title=member.name,
            description=("""
( ͡ ° ͜ʖ ͡ ° )
⠀/ ▌\\
⠀⠀{}
⠀ /  \\
""".format(dick)))
        await ctx.send(embed=message)
        await ctx.send('Nice cock bro! :eggplant:')

    @dsize.error
    async def dsizerror(self, ctx, error):
        await ctx.send('Wrong member.')

def setup(client):
    client.add_cog(Fun(client))
