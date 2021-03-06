import discord
from types import NoneType
from discord.ext import commands, bridge
from essential.config import botcolor

class Events(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Events has been loaded.")

    # @commands.Cog.listener()
    # async def on_command(self, ctx):
    #     if ctx.author != self.client.user:
    #         try:
    #             await ctx.message.delete()
    #         except:
    #             embed = discord.Embed(
    #                 title="Missing Permission.", color=botcolor())
    #             await ctx.channel.send(embed=embed, delete_after=5)
    #             raise commands.BotMissingPermissions("DeleteMessages")
    
    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        self.client.db.child("servers").child(str(guild.id)).set({"DJ-Mode": "False"}, self.client.idToken)
    
    @commands.Cog.listener()
    async def on_member_join(self, member):
        self.client.db.child("servers").child(
            str(member.id)).set({'dj': 'False', 'vc_update': 'False'}, self.client.idToken)

    @commands.Cog.listener()
    async def on_voice_state_update(self,member, before, after):
        if member != self.client.user:
            users = self.client.db.child("users").get(self.client.idToken).val()
            if isinstance(before.channel, NoneType):
                for a in users:
                    user = await self.client.fetch_user(int(a))
                    if user == member:
                        pass
                    else:
                        if self.client.db.child('users').child(str(a)).child('vc_update').get(self.client.idToken).val() == "false":
                            pass
                        else:
                            if user in after.channel.members:
                                pass
                            else:
                                embed = discord.Embed(title=f"{member.display_name} has joined {after.channel.name}.",color=botcolor())
                                await user.send(embed=embed)
            else:
                pass

def setup(client):
    client.add_cog(Events(client))
