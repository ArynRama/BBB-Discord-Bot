import discord
from discord.ext import commands

class Owner(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def disable(self, name):
        for a in self.client.commands:
            if name == a.qualified_name:
                a.update(enable=False)
    
    @commands.command()
    async def enable(self, name):
        for a in self.client.commands:
            if name == a.qualified_name:
                a.update(enable=True)
        
def setup(client):
    client.add_cog(Owner(client))