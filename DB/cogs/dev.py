import asyncio
from ctypes import _StructUnionBase
import discord
from os import listdir
from discord.ext import commands, bridge
from os.path import isfile, join
from essential.config import botcolor, devs
class Dev(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    async def cog_check(self, ctx: bridge.BridgeContext):
        if str(ctx.author.id) in devs():
            return True
        else:
            return False
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("Dev has been loaded.")
        guilds = self.client.guilds
        servers = self.client.db.child("servers").get().val()
        for i in guilds:
            if str(i.id) in servers:
                pass
            else:
                self.client.db.child("servers").child(str(i.id)).set(
                    {"DJ-Only": "False", "DJ-Role": "None"})

    @bridge.bridge_command(aliases=["shutdown", "logout"])
    async def kill(self, ctx: bridge.BridgeContext):
        """Shutsdown the bot."""
        
        embed = discord.Embed(
            title="Bot is disconnecting.", color=botcolor())
        await ctx.send(embed=embed, delete_after=5)
        await self.client.change_presence(status=discord.Status.offline)
        await self.client.close()
    
    @bridge.bridge_command()
    async def cog(self, ctx: bridge.BridgeContext, subcommand = "None", cog = "None"):
        enable_aliases=["activate", "a", "e","load","l", "enable"]
        reload_aliases=["reactivate","r","reenable", "reload"]
        disable_aliases=["deactivate","d","u","disable", "unload"]
        mypath="./DB/cogs"
        cogs = [cogg for cogg in listdir(mypath) if isfile(join(mypath, cogg))]
        cogg = "cogs."+cog.lower()
        check = cogg.lower() + ".py"
        if subcommand == "None":
            embed=discord.Embed(title="Cogs", color=botcolor())
            command = f"```prolog\nEnable\nUnload\nReload```"
            embed.add_field(name="Sub-Commands", value=command)
            await ctx.send(embed=embed, delete_after=5)
        elif subcommand not in enable_aliases or subcommand not in disable_aliases or subcommand not in reload_aliases or subcommand != "add":
            embed=discord.Embed(title="Invalid Subcommand.", color=botcolor())
            await ctx.send(embed=embed, delete_after=5)
        elif cog == "None":
            embed=discord.Embed(title="Please add a cog.", color=botcolor())
            await ctx.send(embed=embed, delete_after=5)
        elif check in cogs:
            if subcommand in enable_aliases:
                self.client.load_extension(cogg)
                embed = discord.Embed(title=f"Loaded {cog.lower()}.", color=botcolor())
                await ctx.send(embed=embed, delete_after=5)
            elif subcommand in disable_aliases:
                self.client.unload_extension(cogg)
                embed = discord.Embed(
                    title=f"Unloaded {cog.lower()}.", color=botcolor())
                await ctx.send(embed=embed, delete_after=5)
            elif subcommand in reload_aliases:
                self.client.unload_extension(cog)
                self.client.load_extension(cog)
                embed = discord.Embed(
                    title=f"Reloaded {cog.lower()}.", color=botcolor())
                await ctx.send(embed=embed, delete_after=5)
            elif subcommand == "add":
                self.client.add_cog(cog)
                embed = discord.Embed(
                    title=f"Added {cog.lower()}.", color=botcolor())
                await ctx.send(embed=embed, delete_after=5)
        else:
            embed = discord.Embed(
                title=f"{cog.title()} is not a valid cog.", color=botcolor())
            await ctx.send(embed=embed, delete_after=5)
    
    bridge.bridge_command()
    async def update_users(self, ctx):
        users = self.client.db.child('users').get().val()
        for guild in self.client.guilds:
            for member in guild.members:
                if member.id in users:
                    pass
                else:
                    self.client.db.child('users').child(str(member.id)).set(
                        {'dj': 'False', 'vc_update': 'False'})
                await asyncio.sleep(2)
        embed = discord.Embed(title="Updated users.", color=botcolor())
        await ctx.send(embed=embed, delete_after=5)

    bridge.bridge_command()
    async def update_servers(self, ctx):
        guilds = self.client.db.child('servers').get().val()
        for guild in self.client.guilds:
            if guild.id in guilds:
                pass
            else:
                self.client.db.child('users').child(str(guild.id)).set(
                    {'DJ-Only': 'False', 'DJ-Role': 'None'})
        embed = discord.Embed(title="Updated servers.", color=botcolor())
        await ctx.send(embed=embed, delete_after=5)

def setup(client):
    client.add_cog(Dev(client))