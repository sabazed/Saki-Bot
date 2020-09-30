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

    @commands.command()
    async def hot(self, ctx):
        reddit = praw.Reddit(client_id=os.environ['client_id'],
                        client_secret=os.environ['client_secret'],
                        username=os.environ['username'],
                        password=os.environ['redditpass'],
                        user_agent='redditmeme.py')
        
        submsn = random.choice(['BeautifulFemales', 'PrettyGirls', 'sexygirls', 'Models'])
        subreddit = reddit.subreddit(submsn)
        submissions = subreddit.hot(limit=50)

        pics = []

        for submission in submissions:
            if submsn != 'sexygirls':
                if submission.over_18:
                    pass
                else:
                    pics.append(submission)
            else:
                pics.append(submission)
        pic = random.choice(pics)
        name = pic.title
        url = pic.url
            
        embed = discord.Embed(title=name)
        embed.set_image(url=url)

        await ctx.send(embed=embed)
        
    @hot.error
    async def hoterror(self, ctx, error):
        await ctx.send('Can\'t generate a picture. Please, try again.')

def setup(client):
    client.add_cog(Fun(client))