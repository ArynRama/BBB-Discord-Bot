import asyncio
import discord
from os import listdir
from discord.ext import commands, bridge
from os.path import isfile, join
from essential.config import botcolor, devs
class Dev(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    async def cog_check(self, ctx: commands.Context):
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
    async def kill(self, ctx: commands.Context):
        """Shutsdown the bot."""
        embed = discord.Embed(
            title="Bot is disconnecting.", color=botcolor())
        await ctx.send(embed=embed, delete_after=5)
        await self.client.change_presence(status=discord.Status.offline)
        await self.client.close()
    
    @commands.group(invoke_without_command=True, name="cog")
    async def cogs(self, ctx: commands.Context):
            embed=discord.Embed(title="Cogs", color=botcolor())
            command = f"```prolog\nEnable\nUnload\nReload```"
            embed.add_field(name="Sub-Commands", value=command)
            await ctx.send(embed=embed, delete_after=5)

    @cogs.command(aliases=["activate", "a", "e","load","l"])
    async def enable(self, ctx: commands.Context, args: str):
        mypath="./DB/cogs"
        cogs = [cog for cog in listdir(mypath) if isfile(join(mypath, cog))]
        cog = "cogs."+args.lower()
        check = args.lower() + ".py"
        if check in cogs:
            self.client.load_extension(cog)
            embed = discord.Embed(title=f"Loaded {args.lower()}.", color=botcolor())
            await ctx.send(embed=embed, delete_after=5)
        else:
            embed = discord.Embed(
                title=f"{args.title()} is not a valid cog.", color=botcolor())
            await ctx.send(embed=embed, delete_after=5)

    @cogs.command(aliases=["deactivate","d","u","disable"])
    async def unload(self,ctx: commands.Context,args: str):
        mypath = "./DB/cogs"
        cogs = [cog for cog in listdir(mypath) if isfile(join(mypath, cog))]
        check = args.lower() + ".py"
        cog = "cogs."+args.lower()
        if check in cogs:
            self.client.unload_extension(cog)
            embed = discord.Embed(
                title=f"Unloaded {args.lower()}.", color=botcolor())
            await ctx.send(embed=embed, delete_after=5)
        else:
            embed = discord.Embed(
                title=f"{args.title()} is not a valid cog.", color=botcolor())
            await ctx.send(embed=embed, delete_after=5)
    
    @cogs.command(aliases=["reactivate","r","reenable"])
    async def reload(self,ctx: commands.Context,args: str):
        mypath = "./DB/cogs"
        cogs = [cog for cog in listdir(mypath) if isfile(join(mypath, cog))]
        check = args.lower() + ".py"
        cog = "cogs." + args.lower()
        if check in cogs:
            self.client.unload_extension(cog)
            self.client.load_extension(cog)
            embed = discord.Embed(
                title=f"Reloaded {args.lower()}.", color=botcolor())
            await ctx.send(embed=embed, delete_after=5)
        else:
            embed = discord.Embed(
                title=f"{args.title()} is not a valid cog.", color=botcolor())
            await ctx.send(embed=embed, delete_after=5)
    
    @cogs.command()
    async def add(self, ctx: commands.Context, args: str):
        cog = args
        self.client.add_cog(cog)
        embed = discord.Embed(
            title=f"Added {args.lower()}.", color=botcolor())
        await ctx.send(embed=embed, delete_after=5)
    
    @bridge.bridge_command()
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

    @bridge.bridge_command()
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