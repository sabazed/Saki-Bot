import discord
import os
import random
from discord.ext import commands, tasks

client = commands.Bot(command_prefix='s/')
client.remove_command('help')
status = ['h3ll0fr1end.wav', 'd3bug.mkv', 'da3m0ns.mp4', '3xpl0its.wmv', 'k3rnel-pan1c.ksd', 'logic-b0mb.hc',
          'm4ster-s1ave.aes', 'h4ndshake.sme', 'succ3ss0r.p12', 'init_5.fve', 'h1dden-pr0cess.axx', 'runtime-error.r00', 'shutdown -r']


@client.event
async def on_ready():
    print('Bot is online')
    change_status.start()


@tasks.loop(seconds=300)
async def change_status():
    await client.change_presence(activity=discord.Game(random.choice(status)))


@client.command()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')


@client.command()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')


@client.command(pass_context=True)
async def help(ctx):
    embed = discord.Embed(
        title='**SakiMeister Help Board**',
        description='**User Commands:**\ns/mine [size] - generates a minesweeper board, default size 8x8\ns/rps - Play \'Rock Paper Scissors\' against the bot\ns/random [X][Y] - Generate a random number between X and Y\n s/gayrate [member] - Rates how much gay the user is\ns/simprate [member] - Rates how much simp the user is\ns/dicksize [member] - Measures the dick size of the user\ns/ttt [member] - Tic Tac Toe game against a member\ns/ff - Generates a random fact'
    )
    await ctx.send(embed=embed)


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

client.run(os.environ['token'])
