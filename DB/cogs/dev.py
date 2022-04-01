import discord
from os import listdir
from os.path import isfile, join
from discord.ext import commands
from cogs.config import Config

class Dev(commands.Cog):
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
    
    @commands.group(name="cog")
    async def cogs(self, ctx, arg):
        if ctx.invoked_subcommand is None:
            embed=discord.Embed(title="Incomplete command passed.", color=Config.botcolor())
            await ctx.send('Invalid git command passed...')

    @cogs.command(alias=["activate", "a", "e"])
    async def enable(self, ctx, args: str):
        mypath="./DB/cogs"
        cogs = [cog for cog in listdir(mypath) if isfile(join(mypath, cog))]
        cog = args.lower()+".py"
        if cog in cogs:
            self.client.add_cog(cog)
            embed = discord.Embed(title=f"Loaded {args.lower()}.", color=Config.botcolor())
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title=f"{args.title()} is not a valid cog.", color=Config.botcolor())
            await ctx.send(embed=embed)

    @cogs.command(alias=["deactivate","d","u"])
    async def unload(self,ctx,args: str):
        mypath = "./DB/cogs"
        cogs = [cog for cog in listdir(mypath) if isfile(join(mypath, cog))]
        cog = args.lower()+".py"
        if cog in cogs:
            self.client.remove_cog(cog)
            embed = discord.Embed(
                title=f"Unloaded {args.lower()}.", color=Config.botcolor())
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title=f"{args.title()} is not a valid cog.", color=Config.botcolor())
            await ctx.send(embed=embed)
    
    @cogs.command(alias=["reactivate","r"])
    async def reload(self,ctx,args: str):
        mypath = "./DB/cogs"
        cogs = [cog for cog in listdir(mypath) if isfile(join(mypath, cog))]
        cog = args.lower()+".py"
        if cog in cogs:
            self.client.remove_cog(cog)
            self.client.add_cog(cog)
            embed = discord.Embed(
                title=f"Reloaded {args.lower()}.", color=Config.botcolor())
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title=f"{args.title()} is not a valid cog.", color=Config.botcolor())
            await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Dev(client))