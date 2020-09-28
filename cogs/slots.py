import discord
import random
import os
import asyncio
import asyncpg
import datetime

from discord.ext import commands

class Fun(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Loaded cog: {__name__[5:]}')

    @commands.command(aliases=['slots'])
    async def slot(self, ctx, bet):
        bet = int(bet)
        symbols = {0: ':eggplant:', 1: ':peach:', 2: ':cherries:', 3: ':black_joker:',  4: ':star:', 5: ':four_leaf_clover:', 6: ':gem:', 7: ':fleur_de_lis:'}
        values = {':peach:': 0.5, ':eggplant:': 0.5, ':black_joker:': 1.5, ':cherries:': 1, ':star:': 3, ':four_leaf_clover:': 10, ':gem:': 25}
        connection = await asyncpg.connect(database=os.environ['database'], host=os.environ['host'], user=os.environ['user'], password=os.environ['password'], port=os.environ['port'])
        content = await connection.fetch('''SELECT * FROM data''')
        playerlist = [i[0] for i in content]
        if str(ctx.author.id) not in playerlist:
            time = datetime.datetime.now()
            delta = datetime.timedelta(hours=8)
            daily = time - delta
            async with connection.transaction():
                await connection.execute("INSERT INTO data VALUES($1, $2, $3, $4)", str(ctx.author.id), 500, 0, daily)
        content = await connection.fetch('''SELECT * FROM data''')
        playerlist = [i[0] for i in content]
        inx = playerlist.index(f'{ctx.author.id}')
        id = content[inx][0]
        balance = int(content[inx][1])
        win = int(content[inx][2])
        if balance < bet:
            await ctx.send('You don\'t have enough balance.')
            await connection.close()
            return
        else:
            embed = discord.Embed(title=':game_die:  **Slot Machine**  :game_die:',
                                    description=f"""
⠀⠀⠀:slot_machine:⠀:slot_machine:⠀:slot_machine: 
⠀⠀⠀:arrows_clockwise:⠀:arrows_clockwise:⠀:arrows_clockwise:
⠀⠀⠀:slot_machine:⠀:slot_machine:‏‏‎‏‏‎‏‏‎⠀:slot_machine:‏‏‎‏‏‎

{ctx.author.mention}'s bet: {bet} :coin:""",
                                    colour=discord.Colour.red())
            msg = await ctx.send(embed=embed)
            balance -= bet
            oldbalance = balance
            slotchars = [0, 1, 2, 3, 4, 5, 6, 7]
            slot1 = random.choices(slotchars, weights=[22, 22, 19, 15, 10, 5, 3, 4])[0]
            embed.description = f"""
⠀⠀⠀:slot_machine:‏‏‎⠀:slot_machine:⠀:slot_machine: 
⠀⠀⠀{symbols[slot1]}⠀:arrows_clockwise:⠀:arrows_clockwise:
⠀⠀⠀:slot_machine:‏‏‎‏‏‎⠀:slot_machine:⠀:slot_machine:‏‏‎‏‏‎

{ctx.author.mention}'s bet: {bet} :coin:"""                       
            await asyncio.sleep(0.7)
            await msg.edit(embed=embed)
            slot2 = random.choices(slotchars, weights=[22, 22, 19, 15, 10, 5, 3, 4])[0]
            embed.description = f"""
⠀⠀⠀:slot_machine:‏‏‎⠀:slot_machine:⠀:slot_machine: 
⠀⠀⠀{symbols[slot1]}⠀{symbols[slot2]}⠀:arrows_clockwise:
⠀⠀⠀:slot_machine:‏‏‎‏‏‎⠀:slot_machine:‏‏‎‏‏‎‏‏‎⠀:slot_machine:‏‏‎‏‏‎

{ctx.author.mention}'s bet: {bet} :coin:"""
            await asyncio.sleep(0.7)
            await msg.edit(embed=embed)
            slot3 = random.choices(slotchars, weights=[22, 22, 19, 15, 10, 5, 3, 4])[0]
            slots = [slot1, slot2, slot3]
            embed.description = f"""
⠀⠀⠀:slot_machine:‏‏⠀:slot_machine:⠀:slot_machine: 
⠀⠀⠀{symbols[slot1]}⠀{symbols[slot2]}⠀{symbols[slot3]}
⠀⠀⠀:slot_machine:‏‏‎‏‏‎⠀:slot_machine:‏‏‎‏‏‎‏‏‎⠀:slot_machine:‏‏‎‏‏‎

{ctx.author.mention}'s bet: {bet} :coin:"""
            await asyncio.sleep(0.7)
            await msg.edit(embed=embed)
            if slots.count(7) == 3:
                balance += bet*50
            elif slots.count(7) == 2:
                if 6 in slots:
                    balance += bet*100
                else:
                    balance += bet*50
            elif slots.count(7) == 1:
                if slot1 == 7:
                    if slot2==slot3:
                        symbol = symbols[slot2]
                        value = values[symbol]
                        balance += bet*value*2
                    else:
                        symbol = symbols[max(slot2, slot3)]
                        value = values[symbol]
                        balance += bet*value
                elif slot2 == 7:
                    if slot1==slot3:
                        symbol = symbols[slot1]
                        value = values[symbol]
                        balance += bet*value*2
                    else:
                        symbol = symbols[max(slot1, slot3)]
                        value = values[symbol]
                        balance += bet*value
                else:
                    if slot1==slot2:
                        symbol = symbols[slot1]
                        value = values[symbol]
                        balance += bet*value*2
                    else:
                        symbol = symbols[max(slot2, slot1)]
                        value = values[symbol]
                        balance += bet*value
            elif slot1 == slot2 == slot3:
                symbol = symbols[slot1]
                value = values[symbol]
                balance += bet*value*2
            elif slot1 == slot2:
                symbol = symbols[slot1]
                value = values[symbol]
                balance += bet*value
            elif slot1 == slot3:
                symbol = symbols[slot1]
                value = values[symbol]
                balance += bet*value
            elif slot3 == slot2:
                symbol = symbols[slot2]
                value = values[symbol]
                balance += bet*value                    
            else:
                await ctx.send('You Lose.')
                async with connection.transaction():
                    await connection.execute("""UPDATE data
                                                SET balance = $1,
                                                    win = $2
                                                WHERE id = $3""", balance, win, id)
                await connection.close()
                return
            if win < (balance-oldbalance):
                win = balance-oldbalance
            await ctx.send(f'You won {int(balance-oldbalance)} :coin:')
            async with connection.transaction():
                await connection.execute("""UPDATE data
                                            SET balance = $1,
                                                win = $2
                                            WHERE id = $3""", balance, win, id)
        await connection.close()

    @slot.error
    async def sloterror(self, ctx, error):
        if error in [ValueError, TypeError]:
            await ctx.send('Enter a valid value!')
        else:
            await ctx.send('An error occoured, please contact server\'s administration.')
        print(error)

    @commands.command()
    async def balance(self, ctx, member: discord.Member = None):
        if member == None:
            member = ctx.author
        connection = await asyncpg.connect(database=os.environ['database'], host=os.environ['host'], user=os.environ['user'], password=os.environ['password'], port=os.environ['port'])
        content = await connection.fetch('''SELECT id, balance FROM data''')
        playerlist = [i[0] for i in content]
        if str(member.id) not in playerlist:
            if member == ctx.author:
                await ctx.send('You don\'t have an account yet.')
            else:
                await ctx.send(f'{member.mention} doesn\'t have an account yet.')
        else:
            inx = playerlist.index(str(member.id))
            await ctx.send(f":moneybag: {member.mention}'s balance is {content[inx][1]} :coin:")
        await connection.close()

    @balance.error
    async def balanceerror(self, ctx, error):
        await ctx.send('An error occoured, please contact server\'s administration.')
        print(error)

    @commands.command(aliases=['topwin'])
    async def win(self, ctx, member: discord.Member = None):
        if member == None:
            member = ctx.author
        connection = await asyncpg.connect(database=os.environ['database'], host=os.environ['host'], user=os.environ['user'], password=os.environ['password'], port=os.environ['port'])
        content = await connection.fetch('''SELECT id, win FROM data''')
        playerlist = [i[0] for i in content]
        if str(member.id) not in playerlist:
            if member == ctx.author:
                await ctx.send('You don\'t have an account yet.')
            else:
                await ctx.send(f'{member.mention} doesn\'t have an account yet.')
        else:
            inx = playerlist.index(str(member.id))
            await ctx.send(f":crown: {member.mention}'s won max value of {content[inx][1]} :coin:")
        await connection.close()

    @win.error
    async def winerror(self, ctx, error):
        await ctx.send('An error occoured, please contact server\'s administration.')
        print(error)

    @commands.command()
    async def daily(self, ctx):
        connection = await asyncpg.connect(database=os.environ['database'], host=os.environ['host'], user=os.environ['user'], password=os.environ['password'], port=os.environ['port'])
        content = await connection.fetch('''SELECT id, balance, daily FROM data''')
        playerlist = [i[0] for i in content]
        if str(ctx.author.id) not in playerlist:
            await ctx.send('You don\'t have an account yet.')
        else:
            inx = playerlist.index(str(ctx.author.id))
            time = datetime.datetime.now()
            delta = datetime.timedelta(hours=8)
            daily = time - delta
            if content[inx][2] < daily:
                balance = content[inx][1]
                balance += 250
                daily = datetime.datetime.now()
                async with connection.transaction():
                    await connection.execute("""UPDATE data
                                                SET balance = $1,
                                                    daily = $2
                                                WHERE id = $3""", balance, daily, str(ctx.author.id))
                await ctx.send(f'You have recieved a bonus. Come back in 8 hours for another! :hourglass:')
            else:
                timeleft = content[inx][2] - daily
                hours = timeleft.seconds // 3600
                minutes = (timeleft.seconds - (3600*hours))//60
                await ctx.send(f':hourglass: **{hours} hours and {minutes} minutes** remaining untill your 8-hour bonus. :money_with_wings:')
        await connection.close()

    @daily.error
    async def dailyerror(self, ctx, error):
        await ctx.send('An error occoured, please contact server\'s administration.')
        print(error)

def setup(client):
    client.add_cog(Fun(client))
