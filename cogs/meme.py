import discord
import random
import praw
import os

from discord.ext import commands

class Fun(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Loaded cog: {__name__[5:]}')

    @commands.command(aliases=['rmeme', 'redditmeme'])
    async def meme(self, ctx, subred = 'memes'):
        reddit = praw.Reddit(client_id=os.environ['client_id'],
                        client_secret=os.environ['client_secret'],
                        username=os.environ['username'],
                        password=os.environ['redditpass'],
                        user_agent='redditmeme.py')
        
        subreddit = reddit.subreddit(subred)
        submissions = subreddit.hot(limit=50)

        memes = []

        for submission in submissions:
            memes.append(submission)
        
        meme = random.choice(memes)

        name = meme.title
        url = meme.url
            
        embed = discord.Embed(title=name)
        embed.set_image(url=url)

        await ctx.send(embed=embed)
        
    @meme.error
    async def memeerror(self, ctx, error):
        await ctx.send('Can\'t generate a meme.')

def setup(client):
    client.add_cog(Fun(client))
