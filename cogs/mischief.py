import asyncio
import discord
from discord.ext import commands
from cogs.errors import BlockedError


def embed_contains(embed, text):
    return (text in embed.title)


def message_contains(message, text):
    return text in message.content or any(embed_contains(embed, text) for embed in message.embeds)


class Mischief(commands.Cog):
    def __init__(self, client):
        self.client = client

    

    @commands.Cog.listener()
    async def on_ready(self):
        print("Mischief has been loaded.")


    @commands.command()
    async def annoy(self, ctx, user: discord.Member, times: int = 10):
        """Mentions user alot of times"""
        for a in range(times):
            await ctx.send(user.mention)
            await asyncio.sleep(0.5)
    
    @commands.command()
    async def block(self, ctx, user):
        """Blocks a user from using commands for 10 minutes."""
        if user == "l": 
            print("l")
        else:
            raise BlockedError
def setup(client):
    client.add_cog(Mischief(client))
