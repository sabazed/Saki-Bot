import discord
from discord.ext import commands


class Admin(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if ctx.message.author.guild_permissions.value == 2147483647:
            await ctx.send('Invalid Argument(s)')
        else:
            pass

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def clear(self, ctx, amount=1):
        await ctx.channel.purge(limit=amount)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def kick(self, ctx, user: discord.Member, *, reason=None):
        await user.kick(reason=reason)
        await ctx.send(f"{user} have been kicked sucessfully")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def ban(self, ctx, user: discord.Member, *, reason=None):
        await user.ban(reason=reason)
        await ctx.send(f"{user} have been bannned sucessfully")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def unban(self, ctx, *, member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')

        for ban_entry in banned_users:
            user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f"{user} have been unbanned sucessfully")
            return

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def ping(self, ctx):
        await ctx.send(f'Pong! {round(self.client.latency * 1000)}ms')


def setup(client):
    client.add_cog(Admin(client))
