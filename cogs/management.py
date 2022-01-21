import discord
from discord.ext import commands
import json
from cogs.config import Config



class NotDev(commands.CommandError):
    pass


class Management(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Management has been loaded.")


    @commands.command()
    async def clear(self, ctx, amount: int):
        """Clears messages in channel."""
        await ctx.channel.purge(limit=amount)


def setup(client):
    client.add_cog(Management(client))
