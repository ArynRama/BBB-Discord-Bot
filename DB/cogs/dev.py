import asyncio
import discord
from os import listdir
from os.path import isfile, join
from discord.ext import commands, bridge
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
        servers = self.client.db.child("servers").get(self.client.idToken).val()
        for i in guilds:
            if str(i.id) in servers:
                pass
            else:
                self.client.db.child("servers").child(str(i.id)).set(
                    {"DJ-Only": "False", "DJ-Role": "None"}, self.client.idToken)

    @bridge.bridge_command(aliases=["shutdown", "logout"])
    async def kill(self, ctx: bridge.BridgeContext):
        """Shutsdown the bot."""
        
        embed = discord.Embed(
            title="Bot is disconnecting.", color=botcolor())
        await ctx.respond(embed=embed, delete_after=5)
        await self.client.change_presence(status=discord.Status.offline)
        await self.client.close()

    @bridge.bridge_command()
    async def cog(self, ctx: bridge.BridgeContext, Subcommand:discord.Option(str, "Subcommand you want to execute", default = "None", choices= ["load", "unload", "reload", "add"]), cog = "None"):
        """Controll the cogs."""
        enable_aliases=["activate", "a", "e","load","l", "enable"]
        reload_aliases=["reactivate","r","reenable", "reload"]
        disable_aliases=["deactivate","d","u","disable", "unload"]
        mypath="./DB/cogs"
        cogs = [cogg for cogg in listdir(mypath) if isfile(join(mypath, cogg))]
        cogg = "cogs."+cog.lower()
        check = cogg.lower() + ".py"
        if Subcommand == "None":
            embed=discord.Embed(title="Cogs", color=botcolor())
            command = f"```prolog\nEnable\nUnload\nReload\nList\nAdd```"
            embed.add_field(name="Sub-Commands", value=command)
            await ctx.respond(embed=embed, delete_after=15)
        elif Subcommand not in enable_aliases or Subcommand not in disable_aliases or Subcommand not in reload_aliases or Subcommand != "add":
            embed=discord.Embed(title="Invalid Subcommand.", color=botcolor())
            await ctx.respond(embed=embed, delete_after=5)
        elif cog == "None":
            embed=discord.Embed(title="Please add a cog.", color=botcolor())
            await ctx.respond(embed=embed, delete_after=5)
        elif check in cogs:
            if Subcommand in enable_aliases:
                self.client.load_extension(cogg)
                embed = discord.Embed(title=f"Loaded {cog.lower()}.", color=botcolor())
                await ctx.respond(embed=embed, delete_after=5)
            elif Subcommand in disable_aliases:
                self.client.unload_extension(cogg)
                embed = discord.Embed(
                    title=f"Unloaded {cog.lower()}.", color=botcolor())
                await ctx.respond(embed=embed, delete_after=5)
            elif Subcommand in reload_aliases:
                self.client.unload_extension(cog)
                self.client.load_extension(cog)
                embed = discord.Embed(
                    title=f"Reloaded {cog.lower()}.", color=botcolor())
                await ctx.respond(embed=embed, delete_after=5)
            elif Subcommand == "add":
                self.client.add_cog(cog)
                embed = discord.Embed(
                    title=f"Added {cog.lower()}.", color=botcolor())
                await ctx.respond(embed=embed, delete_after=5)
        else:
            embed = discord.Embed(
                title=f"{cog.title()} is not a valid cog.", color=botcolor())
            await ctx.respond(embed=embed, delete_after=5)
    
    bridge.bridge_command()
    async def update_users(self, ctx):
        users = self.client.db.child('users').get(self.client.idToken).val()
        for guild in self.client.guilds:
            for member in guild.members:
                if member.id in users:
                    pass
                else:
                    self.client.db.child('users').child(str(member.id)).set(
                        {'dj': 'False', 'vc_update': 'False'}, self.client.idToken)
                await asyncio.sleep(2)
        embed = discord.Embed(title="Updated users.", color=botcolor())
        await ctx.respond(embed=embed, delete_after=5)

    bridge.bridge_command()
    async def update_servers(self, ctx):
        guilds = self.client.db.child('servers').get(self.client.idToken).val()
        for guild in self.client.guilds:
            if guild.id in guilds:
                pass
            else:
                self.client.db.child('users').child(str(guild.id)).set(
                    {'DJ-Only': 'False', 'DJ-Role': 'None'}, self.client.idToken)
        embed = discord.Embed(title="Updated servers.", color=botcolor())
        await ctx.respond(embed=embed, delete_after=5)

def setup(client):
    client.add_cog(Dev(client))