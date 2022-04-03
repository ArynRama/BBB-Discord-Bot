import discord
import json
from essential.config import botcolor
from discord.ext import commands

class Events(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Events has been loaded.")
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author != self.client.user:
            if message.content.startswith("-"):
                try:
                    await message.delete()
                except:
                    embed = discord.Embed(
                        title="Missing Permission.", color=botcolor())
                    await message.channel.send(embed=embed, delete_after=5)
                    raise commands.BotMissingPermissions("DeleteMessages")
    
    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        with open("json/settings.json") as f:
            file = json.load(f)
            file[guild.id] = {
                "DJ-Mode": "False"
            }

def setup(client):
    client.add_cog(Events(client))
