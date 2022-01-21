import main
import discord

from cogs.config import Config
from cogs.errors import NotDev
from discord.ext import commands
class Dev(commands.Cog):
    """Developer only commands."""
    def __init__(self, client):
        self.client = client

    async def cog_check(self, ctx):
        if await self.client.is_owner(ctx.author):
            return True
        #elif await Config.devs() == str(ctx.author.id):
        #    return True
        #elif str(ctx.author.id) in await Config.devs():
        #    return True
        else:
            raise NotDev("Not a dev.")

    @commands.Cog.listener()
    async def on_ready(self):
        print("Dev has been loaded.")

    @commands.group(pass_context=True)
    async def bot(self, ctx):
        """Controll the bot"""
        if ctx.invoked_subcommand == None:
            embed = discord.Embed(title = "restart or disconnect the bot", color = Config.botcolor())
            await ctx.send(embed = embed, delete_after=10)

    @bot.command()
    async def restart(self, ctx):
        """Restarts the bot."""
        embed = discord.Embed(title="Restarting bot...", color=Config.botcolor())
        await ctx.send(embed=embed)
        embed.add_field(name="Restarted by",
                        value=f"{ctx.author}({ctx.author.id})")
        await self.client.fetch_channel(self.client, 887472179749462076).send(embed=embed)

    
    @bot.command(aliases=["shutdown", "logout"])
    async def disconnect(self, ctx):
        """Shutsdown the bot."""
        embed = discord.Embed(
            title="Bot is disconnecting.", color=Config.botcolor())
        await ctx.send(embed=embed, delete_after=5)
        await self.client.change_presence(status=discord.Status.offline)
        await self.client.close()

    @commands.group(pass_context=True)
    async def cog(self, ctx):
        """Controll Cogs"""
        if ctx.invoked_subcommand == None:
            embed = discord.Embed(title = "Load, unload or reload cogs", color = Config.botcolor())
            await ctx.send(embed = embed, delete_after=10)

    @cog.command()
    async def load(self, ctx, extension: str):
        """Loads an extension."""
        if extension in main.LoadCogs.extentions:
            try:
                embed = discord.Embed(
                    title=f"{extension.title()} loaded.", color=Config.botcolor())
                self.client.load_extension(f"cogs.{extension.lower()}")
                print(f"{extension.title()} has been loaded")
                await ctx.send(embed=embed, delete_after=5)
            except Exception as e:
                exc = '{}: {}'.format(type(e).__name__, e)
                print('Failed to load extention {}\n{}'.format(
                    extension.title(), exc))
                embed = discord.Embed(
                    title=f"Something went wrong.", description="Check console for more info", color=Config.botcolor())
                await ctx.send(embed=embed, delete_after=5)
        else:
            embed = discord.Embed(
                title=f"{extension.title()} is not a valid extention.", color=Config.botcolor())
            await ctx.send(embed=embed, delete_after=5)

    @cog.command()
    async def reload(self, ctx, extension: str):
        """Reloads an extension."""
        if extension in main.LoadCogs.extentions or extension in main.LoadCogs.dependencies:
            try:
                embed = discord.Embed(title=f"{extension.title()} reloaded.", color=Config.botcolor())
                self.client.unload_extension(f"cogs.{extension.lower()}")
                self.client.load_extension(f"cogs.{extension.lower()}")
                print(f"{extension.title()} has been reloaded")
                await ctx.send(embed=embed, delete_after=5)
            except Exception as e:
                exc = '{}: {}'.format(type(e).__name__, e)
                print('Failed to load extention {}\n{}'.format(
                    extension.title(), exc))
                embed = discord.Embed(
                    title=f"Something went wrong.", description="Check console for more info", color=Config.botcolor())
                await ctx.send(embed=embed, delete_after=5)
        else:
            embed = discord.Embed(title=f"{extension.title()} is not a valid extention.", color=Config.botcolor())
            await ctx.send(embed=embed, delete_after=5)

    @cog.command()
    async def unload(self, ctx, extension: str):
        """Unloads an extension."""
        if extension in main.LoadCogs.extentions:
            try:
                embed = discord.Embed(
                    title=f"{extension.title()} unloaded.", color=Config.botcolor())
                self.client.unload_extension(f"cogs.{extension.lower()}")
                print(f"{extension.title()} has been unloaded")
                await ctx.send(embed=embed, delete_after=5)
            except Exception as e:
                exc = '{}: {}'.format(type(e).__name__, e)
                print('Failed to unload extention {}\n{}'.format(
                    extension.title(), exc))
                embed = discord.Embed(
                    title=f"Something went wrong.", description="Check console for more info", color=Config.botcolor())
                await ctx.send(embed=embed, delete_after=5)
        else:
            embed = discord.Embed(
                title=f"{extension.title()} is not a valid extention.", color=Config.botcolor())
            await ctx.send(embed=embed, delete_after=5)

    @commands.command()
    async def test(self, ctx):
        """A command to see if bot is working"""
        embed = discord.Embed(title="Bot is working.", color=Config.botcolor())
        await ctx.send(embed=embed, delete_after=5)
        print("working.")
    
def setup(client):
    client.add_cog(Dev(client))
