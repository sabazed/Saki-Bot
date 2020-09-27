import discord
import asyncio
import random

from discord.ext import commands

class Fun(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Loaded cog: {__name__[5:]}')


    @commands.command()  # ROCK PAPER SCISSORS
    async def rps(self, ctx):
        comp = random.randint(1, 3)
        embed = discord.Embed(
            title="**Choose your figure:**", description="\n\n1) Rock :new_moon:\n\n2) Paper :page_facing_up:\n\n3) Scissors :scissors:\n\n(_ex:  s/rock_)", colour=discord.Colour.blue())
        await ctx.send(embed=embed)
        figures = {1: 'rock', 2: 'paper', 3: 'scissors'}
        msg = await self.client.wait_for('message', check=lambda message: message.author == ctx.author, timeout=10)
        if msg.content.lower() == "rock" or str(msg.content).lower() == "1":
            usr = 1
        elif msg.content.lower() == "paper" or str(msg.content).lower() == "2":
            usr = 2
        elif msg.content.lower() == "scissors" or str(msg.content).lower() == "3":
            usr = 3
        else:
            await ctx.send('Wrong response.')
            return
        timer = 0
        while usr == 0:
            await asyncio.sleep(3)
            timer += 3
            if timer > 10:
                await ctx.send('Game Over.')
                return
        await ctx.send('You chose **{}**.\n'.format(figures[usr]))
        await asyncio.sleep(1.5)
        await ctx.send("I chose **{}**!\n".format(figures[comp]))
        await asyncio.sleep(1)
        if comp == usr:
            await ctx.send("It's a **tie!** :necktie: :clown:")
        elif abs(comp - usr) == 1:
            if comp > usr:
                await ctx.send('I won! :partying_face: ')
            else:
                await ctx.send('You win! :flag_white: ')
        elif abs(comp - usr) == 2:
            if comp < usr:
                await ctx.send('I won! :partying_face: ')
            else:
                await ctx.send('You win! :flag_white: ')

    @rps.error
    async def rpserror(self, ctx, error):
        await ctx.send('Game Over.')

def setup(client):
    client.add_cog(Fun(client))