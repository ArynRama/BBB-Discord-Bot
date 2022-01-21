import json
import discord
from cogs.config import Config
from discord.ext import commands

class NotDev(commands.CommandError):
    pass

class InvalidArgment(commands.CommandError):
    pass


class BlockedError(commands.CommandError):
    pass

class HelpfulError(commands.CommandError):
    pass

class Blacklisted_Channel(commands.CommandError):
    pass

class Blacklisted_User(commands.CommandError):
    pass

class Errors(commands.Cog, description= "Errors"):

    def __init__(self, client):
        self.client = client



    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, NotDev):
            embed = discord.Embed(title=f"You are not a developer.", color=Config.botcolor())
            await ctx.send(embed=embed, delete_after=5)
            print(f"{ctx.author.name}({ctx.author.id}) tried to use a dev command.")
        elif isinstance(error, BlockedError):
            embed = discord.Embed(
                title=f"You are blocked.", color=Config.botcolor())
            print("blocked.")
            await ctx.send(embeds=embed, delete_after=5)
        elif isinstance(error, commands.CommandNotFound):
            embed = discord.Embed(
                title=f"Command not found.", color=Config.botcolor())
            await ctx.send(embed=embed, delete_after=5)
        elif isinstance(error, commands.DisabledCommand):
            embed = discord.Embed(
                title=f"Command is disabled.", color=Config.botcolor())
            await ctx.send(embed=embed, delete_after=5)
        elif isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                title=f"You have insuffisient permissions.", color=Config.botcolor())
            await ctx.send(embed=embed, delete_after=5)

            



def setup(client):
    client.add_cog(Errors(client))
