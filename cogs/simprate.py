import discord
import random

from discord.ext import commands

class Fun(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Loaded cog: {__name__[5:]}')

    @commands.command(aliases=['simp', 'howsimp', 'srate'])  # SIMP RATE
    async def simprate(self, ctx, member: discord.Member = None):
        simpnum = random.randint(0, 100)
        if member == None:
            if simpnum >= 75:
                if simpnum == 100:
                    message = str(
                        f'You are {simpnum}% complete :regional_indicator_s: :regional_indicator_i: :regional_indicator_m: :regional_indicator_p: ')
                else:
                    message = str(
                        f'You are {simpnum}% simp! :sweat_drops:')
            else:
                message = str(f'You are {simpnum}% simp.')
        else:
            if simpnum >= 75:
                if simpnum == 100:
                    message = str(
                        f'{member.mention} is {simpnum}% an ultimate :regional_indicator_s: :regional_indicator_i: :regional_indicator_m: :regional_indicator_p:')
                else:
                    message = str(
                        f'{member.mention} is {simpnum}% simp! :sweat_drops:')
            else:
                message = str(f'{member.mention} is {simpnum}% simp.')
        await ctx.send(message)

    @simprate.error
    async def simperror(self, ctx, error):
        await ctx.send('Wrong member.')

def setup(client):
    client.add_cog(Fun(client))