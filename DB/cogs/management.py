import discord
from discord.ext import commands

from DB.essential.config import botcolor
from ..essential.checks import is_dev

class Management(commands.Cog):
    def __init__(self, client):
        self.client = client

    commands.command()
    @is_dev
    async def whois(self, ctx, args):
        lookup = self.client.fetch_user(args)
        embed = discord.Embed(title=lookup,color=botcolor())
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Management(client))