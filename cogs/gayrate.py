import discord
import random

from discord.ext import commands

class Fun(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Loaded cog: {__name__[5:]}')

    @commands.command(aliases=['gay', 'howgay', 'grate'])  # GAY RATE
    async def gayrate(self, ctx, member: discord.Member = None):
        gaynum = random.randint(0, 100)
        if member == None:
            if gaynum >= 75:
                if gaynum == 100:
                    message = str(
                        f'You are {gaynum}% total PIDORination. :rainbow:')
                else:
                    message = str(
                        f'You are {gaynum}% gay! PIDOOR :eggplant:')
            else:
                message = str(f'You are {gaynum}% gay.')
        else:
            if gaynum >= 75:
                if gaynum == 100:
                    message = str(
                        f'{member.mention} is {gaynum}% total PIDORination. :rainbow:')
                else:
                    message = str(
                        f'{member.mention} is {gaynum}% gay! PIDOOR :eggplant:')
            else:
                message = str(f'{member.mention} is {gaynum}% gay.')
        await ctx.send(message)

    @gayrate.error
    async def gayerror(self, ctx, error):
        await ctx.send('Wrong member.')

def setup(client):
    client.add_cog(Fun(client))