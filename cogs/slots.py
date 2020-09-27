### ADD DAILY WAGE SYSTEM/8-HOUR CYCLE ###

import discord
import random
import os
import csv
import asyncio

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
        # if type(bet) != int:
        #     await ctx.send('Enter a valid value to bet!')
        #     return
        symbols = {0: ':eggplant:', 1: ':peach:', 2: ':cherries:', 3: ':black_joker:',  4: ':star:', 5: ':four_leaf_clover:', 6: ':gem:', 7: ':fleur_de_lis:'}
        values = {':peach:': 0.5, ':eggplant:': 0.5, ':black_joker:': 1.5, ':cherries:': 1, ':star:': 3, ':four_leaf_clover:': 10, ':gem:': 25}
        with open('players/playerlist.txt', 'r+') as playerlist:
            content = playerlist.readlines()
            if str(str(ctx.author.id) + '\n') not in content:
                playerlist.write(str(ctx.author.id) + '\n')
                with open(f'./players/{ctx.author.id}.csv', 'w+') as newplayer:
                    fieldnames = ('name', 'balance', 'win')
                    csv_writer = csv.DictWriter(newplayer, fieldnames = fieldnames, delimiter = ',')
                    csv_writer.writeheader()
                    csv_writer.writerow({'name': ctx.author.name, 'balance': 500, 'win': 0})
                    await ctx.send('Account created, please try again.')

            else:
                with open(f'./players/{ctx.author.id}.csv', 'r') as tmeplayer:
                    csv_reader = csv.DictReader(tmeplayer, delimiter=',')
                    balance = 0
                    win = 0
                    name = ''
                    for i in csv_reader:
                        name = i['name']
                        balance = int(i['balance'])
                        win = int(i['win'])
                    with open(f'./players/{ctx.author.id}.bak.csv', 'w') as bkplayer:
                        fieldnames = ('name', 'balance', 'win')
                        temp_writer = csv.DictWriter(bkplayer, fieldnames=fieldnames, delimiter=',')
                        temp_writer.writerow({'name': name, 'balance': balance, 'win': win})
                    with open(f'./players/{ctx.author.id}.csv', 'w+') as player:
                        fieldnames = ('name', 'balance', 'win')
                        csv_writer = csv.DictWriter(player, fieldnames=fieldnames, delimiter=',')
                        csv_writer.writeheader()
                        if balance < bet:
                            await ctx.send('You don\'t have enough balance.')
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
                            newemb = discord.Embed(title=':game_die:  **Slot Machine**  :game_die:',
                                                  description=f"""
            
⠀⠀⠀:slot_machine:‏‏‎⠀:slot_machine:⠀:slot_machine: 
⠀⠀⠀{symbols[slot1]}⠀:arrows_clockwise:⠀:arrows_clockwise:
⠀⠀⠀:slot_machine:‏‏‎‏‏‎⠀:slot_machine:⠀:slot_machine:‏‏‎‏‏‎

{ctx.author.mention}'s bet: {bet} :coin:""",
                                                  colour=discord.Colour.red())                            
                            await asyncio.sleep(0.7)
                            await msg.edit(embed=newemb)
                            slot2 = random.choices(slotchars, weights=[22, 22, 19, 15, 10, 5, 3, 4])[0]
                            newemb = discord.Embed(title=':game_die:  **Slot Machine**  :game_die:',
                                                  description=f"""
            
⠀⠀⠀:slot_machine:‏‏‎⠀:slot_machine:⠀:slot_machine: 
⠀⠀⠀{symbols[slot1]}⠀{symbols[slot2]}⠀:arrows_clockwise:
⠀⠀⠀:slot_machine:‏‏‎‏‏‎⠀:slot_machine:‏‏‎‏‏‎‏‏‎⠀:slot_machine:‏‏‎‏‏‎

{ctx.author.mention}'s bet: {bet} :coin:""",
                                                  colour=discord.Colour.red())
                            await asyncio.sleep(0.7)
                            await msg.edit(embed=newemb)
                            slot3 = random.choices(slotchars, weights=[22, 22, 19, 15, 10, 5, 3, 4])[0]
                            slots = [slot1, slot2, slot3]
                            newemb = discord.Embed(title=':game_die:  **Slot Machine**  :game_die:',
                                                  description=f"""
            
⠀⠀⠀:slot_machine:‏‏⠀:slot_machine:⠀:slot_machine: 
⠀⠀⠀{symbols[slot1]}⠀{symbols[slot2]}⠀{symbols[slot3]}
⠀⠀⠀:slot_machine:‏‏‎‏‏‎⠀:slot_machine:‏‏‎‏‏‎‏‏‎⠀:slot_machine:‏‏‎‏‏‎

{ctx.author.mention}'s bet: {bet} :coin:""",
                                                  colour=discord.Colour.red())
                            await asyncio.sleep(0.7)
                            await msg.edit(embed=newemb)
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
                                csv_writer.writerow({'name': name, 'balance': int(balance), 'win': int(win)})
                                return
                            if win < (balance-oldbalance):
                                win = balance-oldbalance
                            await ctx.send(f'You won {int(balance-oldbalance)} :coin:')
                        csv_writer.writerow({'name': name, 'balance': int(balance), 'win': int(win)})

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
        with open(f'./players/{member.id}.csv', 'r') as bfile:
            csv_reader = csv.DictReader(bfile, delimiter=',')
            for i in csv_reader:
                await ctx.send(f":moneybag: {member.mention}'s balance is {i['balance']} :coin:")

    @balance.error
    async def balanceerror(self, ctx, error):
        await ctx.send('An error occoured, please contact server\'s administration.')
        print(error)

    @commands.command(aliases=['topwin'])
    async def win(self, ctx, member: discord.Member = None):
        if member == None:
            member = ctx.author
        with open(f'./players/{member.id}.csv', 'r') as wfile:
            csv_reader = csv.DictReader(wfile, delimiter=',')
            for i in csv_reader:
                await ctx.send(f":crown: {member.mention} has won max of {i['win']} :coin:")

    @win.error
    async def winerror(self, ctx, error):
        await ctx.send('An error occoured, please contact server\'s administration.')
        print(error)

def setup(client):
    client.add_cog(Fun(client))