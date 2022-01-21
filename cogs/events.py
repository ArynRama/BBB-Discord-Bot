import json
import main
import discord
from cogs.config import Config
from discord.ext import commands

class Events(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Events has been loaded.")

    @commands.Cog.listener()
    async def on_guild_join(self,guild):

        print("Joined Guild {guild.name}({guild.id})")

        with open("prefixes.json", "r") as f:
            prefixes = json.load(f)

        prefixes[str(guild.id)] = Config.defaultprefix()

        with open("prefixes.json", "w") as f:
            json.dump(prefixes, f)
    
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
                        
        if isinstance(message.channel, discord.DMChannel):
            if message.embeds == []:
                embed = discord.Embed(
                    title=f"{message.author.name}#{message.author.discriminator} ({message.author.id})", color=Config.botcolor())
                embed.add_field(name="Message", value=f"{message.content}")
                await self.client.get_channel(887472179749462076).send(embed=embed)
                await self.client.get_channel(887472179749462076).send(message)
            else:
                embed = discord.Embed(
                    title=f"{message.author.name}#{message.author.discriminator} ({message.author.id})", color=Config.botcolor())
                embed.add_field(
                    name="Message", value=f"{message.embeds[0].title}")
                await self.client.get_channel(887472179749462076).send(embed=embed)
        else:
            pass
    
    @commands.Cog.listener()
    async def on_voice_state_update(self,member,vb,va):
        owner = await self.client.fetch_user(419848392223621120)
        members = member.voice.channel.members
        if members.__len__() > 0:
            if owner not in members:
                embed = discord.Embed(title=f"{member} has joined {member.voice.channel} in {member.voice.channel.guild}.", color=Config.botcolor())
                await owner.send(embed=embed)
                
def setup(client):
    client.add_cog(Events(client))
