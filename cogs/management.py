import discord
from discord.ext import commands
import json
from cogs.config import Config



class NotDev(commands.CommandError):
    pass


class Management(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Management has been loaded.")

    @commands.command()
    async def setprefix(self, ctx, arg):
        """Changes the prefix in this server."""
        try:
            with open(r"C:\Users\aryan\Documents\Workspace\Bots\DiscordBot2\json\prefixes.json", "r") as f:
                prefixes = json.load(f)

                prefixes[str(ctx.guild.id)] = arg
            with open(r"C:\Users\aryan\Documents\Workspace\Bots\DiscordBot2\json\prefixes.json", "w") as f:
                json.dump(prefixes, f)
            embed = discord.Embed(title=f"Prefix Set to {arg}",color=Config.botcolor())
            await ctx.send(embed=embed, delete_after=5)
        except:
            await ctx.send("Error.")

    @commands.command()
    async def clear(self, ctx, amount: int):
        """Clears messages in channel."""
        await ctx.channel.purge(limit=amount)


def setup(client):
    client.add_cog(Management(client))
