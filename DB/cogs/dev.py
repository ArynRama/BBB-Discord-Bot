import discord
from os import listdir
from os.path import isfile, join
from discord.ext import commands
from cogs.config import Config

class Dev(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    async def cog_check(self, ctx):
        if str(ctx.author.id) in Config.devs():
            return True
        else:
            return False

    @commands.command(aliases=["shutdown", "logout"])
    async def disconnect(self, ctx):
        """Shutsdown the bot."""
        embed = discord.Embed(
            title="Bot is disconnecting.", color=Config.botcolor())
        await ctx.send(embed=embed, delete_after=5)
        await self.client.change_presence(status=discord.Status.offline)
        await self.client.close()
    
    @commands.group(invoke_without_command=True, name="cog")
    async def cogs(self, ctx):
            embed=discord.Embed(title="Cogs", color=Config.botcolor())
            command = f"```prolog\nEnable\nUnload\nReload```"
            embed.add_field(name="Sub-Commands", value=command)
            await ctx.send(embed=embed, delete_after=5)

    @cogs.command(aliases=["activate", "a", "e","load","l"])
    async def enable(self, ctx, args: str):
        mypath="./DB/cogs"
        cogs = [cog for cog in listdir(mypath) if isfile(join(mypath, cog))]
        cog = "cogs."+args.lower()
        check = args.lower() + ".py"
        if check in cogs:
            self.client.add_cog(cog)
            embed = discord.Embed(title=f"Loaded {args.lower()}.", color=Config.botcolor())
            await ctx.send(embed=embed, delete_after=5)
        else:
            embed = discord.Embed(
                title=f"{args.title()} is not a valid cog.", color=Config.botcolor())
            await ctx.send(embed=embed, delete_after=5)

    @cogs.command(aliases=["deactivate","d","u","disable"])
    async def unload(self,ctx,args: str):
        mypath = "./DB/cogs"
        cogs = [cog for cog in listdir(mypath) if isfile(join(mypath, cog))]
        check = args.lower() + ".py"
        cog = "cogs."+args.lower()
        if check in cogs:
            self.client.unload_extension(cog)
            embed = discord.Embed(
                title=f"Unloaded {args.lower()}.", color=Config.botcolor())
            await ctx.send(embed=embed, delete_after=5)
        else:
            embed = discord.Embed(
                title=f"{args.title()} is not a valid cog.", color=Config.botcolor())
            await ctx.send(embed=embed, delete_after=5)
    
    @cogs.command(aliases=["reactivate","r","reenable"])
    async def reload(self,ctx,args: str):
        mypath = "./DB/cogs"
        cogs = [cog for cog in listdir(mypath) if isfile(join(mypath, cog))]
        check = args.lower() + ".py"
        cog = "cogs." + args.lower()
        if check in cogs:
            self.client.unload_extension(cog)
            self.client.load_extension(cog)
            embed = discord.Embed(
                title=f"Reloaded {args.lower()}.", color=Config.botcolor())
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title=f"{args.title()} is not a valid cog.", color=Config.botcolor())
            await ctx.send(embed=embed)
        
    

def setup(client):
    client.add_cog(Dev(client))