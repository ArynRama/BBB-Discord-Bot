import discord
from cogs.config import Config
from discord.ext import commands

class DMs(commands.Cog):
    """Dm members using the bot"""
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("DMs has been loaded.")

    @commands.command(aliases=["send", "dm", "message"])
    async def send_dm(self, ctx, user: discord.User or discord.User.id, *, content):
        """Sends a direct message to the mentioned user as the bot."""
        try:
            embed = discord.Embed(title=content, color=Config.botcolor())
            await user.send(embed=embed)
            embed = discord.Embed(title=f"Sent {content} to {user}", color=Config.botcolor())
            await ctx.send(f"Sent {content} to {user}", delete_after=5)
        except:
            embed = discord.Embed(title="Something went wrong.", color=Config.botcolor())
            await ctx.send(embed=embed,delete_after=5)
        
    

def setup(client):
    client.add_cog(DMs(client))
