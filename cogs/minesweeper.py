import discord
import random

from discord.ext import commands

class Fun(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Loaded cog: {__name__[5:]}')

    @commands.command()  # MINESWEEPER
    async def mine(self, ctx, size=8):
        if size < 6 or size > 14:
            raise CommandInvokeError
        n = int(size)
        board = []
        for i in range(n):
            list1 = []
            for _ in range(n):
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
            board[x].insert(y, ':boom:')
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

def setup(client):
    client.add_cog(Fun(client))