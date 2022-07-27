import asyncio
import discord
from discord.ext import commands, bridge
from essential.config import botcolor


def embed_contains(embed, text):
    return (text in embed.title)


def message_contains(message, text):
    return text in message.content or any(embed_contains(embed, text) for embed in message.embeds)


class Miscellaneous(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Miscellaneous has been loaded.")

    @bridge.bridge_command()
    async def annoy(self, ctx: bridge.BridgeContext, user: discord.Member, times: int = 10):
        """Mentions user alot of times"""
        for a in range(times):
            await ctx.send(user.mention)
            await asyncio.sleep(0.5)
    
    @bridge.bridge_command(aliases=["vcu","vu","voicechannelupdate","update"])
    async def voiceupdate(self, ctx, arg: str = "toggle", user: discord.Member = None):
        author = ctx.author.id
        if user == None:
            subject = ctx.author.id
        else:
            subject = user.id
        ids = self.client.db.child("users").get(self.client.idToken).val()
        if subject in ids:
            value = self.client.db.child("users").child(str(author)).child("vc_update").get(self.client.idToken).val()
            if value == "False":
                if arg == "toggle":
                    self.client.db.child("users").child(str(author)).child("vc_update").set("True", self.client.idToken)
                elif arg == "True":
                    self.client.db.child("users").child(
                        str(author)).child("vc_update").set("True", self.client.idToken)
                else:
                    embed = discord.Embed(
                        title=f"{arg.title()} is not a valid argument.", color=botcolor())
                    await ctx.send(embed=embed, delete_after=5)
            elif value == "True":
                if arg == "toggle":
                    self.client.db.child("users").child(str(author)).child(
                        "vc_update").set("False", self.client.idToken)
                elif arg == "False":
                    self.client.db.child("users").child(str(author)).child(
                        "vc_update").set("False", self.client.idToken)
                else:
                    embed = discord.Embed(title=f"{arg.title()} is not a valid argument.", color=botcolor())
                    await ctx.send(embed=embed, delete_after=5)
            else:
                if user == None:
                    embed = discord.Embed(title=f"User {author} has invalid vc_update value({value}).", color=botcolor())
                else:
                    embed = discord.Embed(title=f"User {user.id} has invalid vc_update value({value}).", color=botcolor())
                ctx.send(embed=embed, delete_after=5)

    

def setup(client):
    client.add_cog(Miscellaneous(client))
