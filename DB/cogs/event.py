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
        with open("json/settings.json", "r") as f:
            file = json.load(f)
        with open("json/settings.json", "w") as f:
            file["settings"][str(guild.id)] = {
                "DJ-Mode": "False"
            }

    @commands.Cog.listener()
    async def on_voice_state_update(self,member, before, after):
        with open("json/settings.json", "r") as f:
            file = json.load(f)
            users= file["users"]
        for a in users:
            if a["message"] == "false":
                pass
            else:
                user = await self.client.fetch_user(a)
                if member != self.client.user:
                    if user in before.channel.members:
                        pass
                    else:
                        embed = discord.Embed(title=f"{member.user} has joined {after.channel.name}.")
                        await user.send(embed=embed)

def setup(client):
    client.add_cog(Events(client))
