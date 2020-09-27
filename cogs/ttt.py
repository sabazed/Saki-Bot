import discord
import random

from discord.ext import commands

class Fun(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Loaded cog: {__name__[5:]}')

    @commands.command(aliases=['tictactoe'])
    async def ttt(self, ctx, member: discord.Member = None):

        if member == None:
            await ctx.send('You should choose another player for this challenge!')
            return

        elif (member == ctx.author) or (member.bot == 1):
            await ctx.send('You should choose another player for this challenge!')
            return

        board = [] #create board
        for i in range(3):
            list1 = []
            for _ in range(3):
                list1.append(0)
            board.append(list1)
        taken = set()
        player = 1
        game = 0
    
        tmp = ''
        for r in board: #print empty board
            for c in r:
                if c == 0:
                    c = ':white_square_button:'
                elif c == 1:
                    c = ':x:'
                else:
                    c = ':o:'
                tmp += ''.join(c)
            tmp += ''.join('\n')

        await ctx.send(f'{ctx.author.mention} has started Tic Tac Toe game against {member.mention}!')
        brd = await ctx.send(tmp)
        message = await ctx.send(f'{ctx.author.display_name}\'s move. Enter a block number [1-9]: ')

        while (game == 0) and ((0 in board[0]) or (0 in board[1]) or (0 in board[2])):

            final = ''
            for r in board: #update board content
                for c in r:
                    if c == 0:
                        c = ':white_square_button:'
                    elif c == 1:
                        c = ':x:'
                    else:
                        c = ':o:'
                    final += ''.join(c)
                final += ''.join('\n')

            if player%2==1:
                playerdisc = ctx.author
            else:
                playerdisc = member
            
            await message.edit(content=f'{playerdisc.display_name}\'s move. Enter a block number [1-9]: ')


            wrongvalueresponse = f"Wrong value... Try again {playerdisc.display_name}"
            takenslotresponse = f'That slot is already used. Try again {playerdisc.display_name}'

            one = board[0][0]
            two = board[0][1]
            three = board[0][2]
            four = board[1][0]
            five = board[1][1]
            six = board[1][2]
            seven = board[2][0]
            eight = board[2][1]
            nine = board[2][2]
            first = [one, two, three]
            second = [four, five, six]
            third = [seven, eight, nine]
            fourth = [one, four, seven]
            fifth = [two, five, eight]
            sixth = [three, six, nine]
            seventh = [one, five, nine]
            eighth = [three, five, seven]
            combs = [first, second, third, fourth, fifth, sixth, seventh, eighth] #combinations to win
            plays = [[1, 1, 1], [2, 2, 2]] # 1=X 2=O

            await brd.edit(content=final)

            for comb in combs:
                for play in plays:
                    if play == comb:
                        if 1 in play: # check if a combination matches the winning 3 figures
                            await ctx.send(f'Congratulations! :partying_face: {ctx.author.mention} won!')
                            game += 1
                            return
                        else:
                            await ctx.send(f'{member.mention} won!')
                            game += 1
                            return
                    else:
                        pass
            if game == 1:
                await ctx.send('Game Over')
                return

            if player == 8: # after 8 moves, if there is no winner, it's a tie.
                await message.edit(content='It\'s a tie!')
                game += 1
                await ctx.send('Game Over. :flag_white:')
                return

            if player%2==1:
                move = await self.client.wait_for('message', check=lambda message: message.author == ctx.author, timeout=10)
            else:
                move = await self.client.wait_for('message', check=lambda message: message.author == member, timeout=10)
            move = int(move.content)
            if not move in [1,2,3,4,5,6,7,8,9]: 
                await message.edit(content=wrongvalueresponse)
                await ctx.channel.purge(limit=1)
                pass
            else:
                await ctx.channel.purge(limit=1)
                if move in taken:
                    player -= 1
                    await message.edit(content=takenslotresponse)
                    pass
                else:
                    taken.add(move)
                    if player % 2 == 1:
                        if move == 1:
                            board[0][0] += 1
                        elif move == 2:
                            board[0][1] += 1
                        elif move == 3:
                            board[0][2] += 1
                        elif move == 4:
                            board[1][0] += 1
                        elif move == 5:
                            board[1][1] += 1
                        elif move == 6:
                            board[1][2] += 1
                        elif move == 7:
                            board[2][0] += 1
                        elif move == 8:
                            board[2][1] += 1
                        elif move == 9:
                            board[2][2] += 1
                        else:
                            player -= 1
                            await message.edit(content=wrongvalueresponse)
                            pass
                    else:
                        if move == 1:
                            board[0][0] += 2
                        elif move == 2:
                            board[0][1] += 2
                        elif move == 3:
                            board[0][2] += 2
                        elif move == 4:
                            board[1][0] += 2
                        elif move == 5:
                            board[1][1] += 2
                        elif move == 6:
                            board[1][2] += 2
                        elif move == 7:
                            board[2][0] += 2
                        elif move == 8:
                            board[2][1] += 2
                        elif move == 9:
                            board[2][2] += 2
                        else:
                            await message.edit(content=wrongvalueresponse)
                            player -= 1
                            pass
            player += 1

    @ttt.error
    async def ttt_error(self, ctx, error):
        if isinstance(error, ValueError):
            await ctx.send('Wrong response, game over.')
        else:
            await ctx.send('Time out! Game Over.')

def setup(client):
    client.add_cog(Fun(client))