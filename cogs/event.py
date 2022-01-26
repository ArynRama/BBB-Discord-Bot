import json
import discord
import main
from cogs.config import Config
from discord.ext import commands

class Events(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Events has been loaded.")
    
    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        with open("json/prefixes.json", "r") as f:
            prefixes = json.load(f)
        
        prefixes[str(guild.id)] = Config.defaultprefix()

        with open("json/prefixes.json", "w") as fw:
            json.dump(f,fw)
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author != self.client.user:
            prefixes = await main.get_prefix(self.client, message)
            for prefix in prefixes:
                if message.content.startswith(prefix):
                    try:
                        await message.delete()
                    except:
                        embed = discord.Embed(
                            title="Missing Permission.", color=Config.botcolor)
                        await message.channel.send(embed=embed, delete_after=5)
                        raise commands.BotMissingPermissions("DeleteMessages")

def setup(client):
    client.add_cog(Events(client))
