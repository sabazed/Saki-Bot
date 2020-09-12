import discord
import random
import time
from discord.ext import commands


class Fun(commands.Cog):

    def __init__(self, client):
        self.client = client

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
            time.sleep(3)
            timer += 3
            if timer > 10:
                await ctx.send('Game Over.')
                return
        await ctx.send('You chose **{}**.\n'.format(figures[usr]))
        time.sleep(1.5)
        await ctx.send("I chose **{}**!\n".format(figures[comp]))
        time.sleep(1)
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

    @commands.command(aliases=['random'])  # RANDOM NUMBER
    async def random_num(self, ctx, start=0, end=1):
        maxn = int(max(start, end))
        minn = int(min(start, end))
        await ctx.send(str(random.randint(minn, maxn)))

    @random_num.error
    async def rndnumerr(self, ctx, error):
        await ctx.send('You should specify two valid numbers.')

    @commands.command()  # MINESWEEPER
    async def mine(self, ctx, size=8):
        if size < 6 or size > 14:
            raise CommandInvokeError
        n = int(size)
        board = []
        for i in range(n):
            list1 = []
            for i in range(n):
                list1.append(0)
            board.append(list1)

        # get random 10 bombs
        bombs = []
        while len(bombs) != round((n * n) / 8):
            x = random.randint(0, n - 1)
            y = random.randint(0, n - 1)
            if [x, y] in bombs:
                pass
            else:
                bombs.append([x, y])

        # put bombs on the board
        for bomb in bombs:
            x = bomb[0]
            y = bomb[1]
            if x == 0 and y == 0:
                board[x][y + 1] += 1
                board[x + 1][y] += 1
                board[x + 1][y + 1] += 1
            elif x == 0 and y == n - 1:
                board[x][y - 1] += 1
                board[x + 1][y] += 1
                board[x + 1][y - 1] += 1
            elif x == n - 1 and y == n - 1:
                board[x][y - 1] += 1
                board[x - 1][y] += 1
                board[x - 1][y - 1] += 1
            elif x == n - 1 and y == 0:
                board[x][y + 1] += 1
                board[x - 1][y] += 1
                board[x - 1][y + 1] += 1
            elif x == 0 and y > 0:
                board[x][y + 1] += 1
                board[x][y - 1] += 1
                board[x + 1][y + 1] += 1
                board[x + 1][y] += 1
                board[x + 1][y - 1] += 1
            elif x == n - 1 and y > 0:
                board[x][y + 1] += 1
                board[x][y - 1] += 1
                board[x - 1][y + 1] += 1
                board[x - 1][y] += 1
                board[x - 1][y - 1] += 1
            elif x > 0 and y == n - 1:
                board[x - 1][y] += 1
                board[x - 1][y - 1] += 1
                board[x][y - 1] += 1
                board[x + 1][y - 1] += 1
                board[x + 1][y] += 1
            elif x > 0 and y == 0:
                board[x - 1][y] += 1
                board[x - 1][y + 1] += 1
                board[x][y + 1] += 1
                board[x + 1][y + 1] += 1
                board[x + 1][y] += 1
            else:
                board[x - 1][y - 1] += 1
                board[x - 1][y] += 1
                board[x - 1][y + 1] += 1
                board[x][y - 1] += 1
                board[x][y + 1] += 1
                board[x + 1][y - 1] += 1
                board[x + 1][y] += 1
                board[x + 1][y + 1] += 1
        for bomb in bombs:
            x = bomb[0]
            y = bomb[1]
            board[x].insert(y, ':bomb:')
            del board[x][y + 1]  # delete existing 0

        final = ''
        for r in board:
            for c in r:
                if c == 0:
                    c = ':zero:'
                elif c == 1:
                    c = ':one:'
                elif c == 2:
                    c = ':two:'
                elif c == 3:
                    c = ':three:'
                elif c == 4:
                    c = ':four:'
                elif c == 5:
                    c = ':five:'
                elif c == 6:
                    c = ':six:'
                elif c == 7:
                    c = ':seven:'
                elif c == 8:
                    c = ':eight:'
                elif c == 9:
                    c = ':nine:'
                final += ''.join('||' + str(c) + '||')
            final += ''.join('\n')
        await ctx.send(f'{n}x{n} board, {round(n*n/8)} bombs generated.\n')
        await ctx.send(final)

    @mine.error
    async def mine_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send('Please specify a valid number!')
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send('Please specify a number between 6 and 14.')

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

    @dsize.error
    async def dsizerror(self, ctx, error):
        await ctx.send('Wrong member.')


def setup(client):
    client.add_cog(Fun(client))
