import discord
from discord.ext import commands

class Events(commands.Cogs):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Events has been loaded.")

def setup(client):
    client.add_cog(Events)
