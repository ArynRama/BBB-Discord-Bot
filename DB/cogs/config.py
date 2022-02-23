from discord import Color
from discord.ext import commands
from configparser import ConfigParser

class Config(commands.Cog):
    def __init__(self,client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Config has been loaded.")

    config = ConfigParser()
    config.read("options.ini")

    def botcolor():
        r = 0
        g = 152
        b = 252
        botcolor = Color.from_rgb(int(r), int(g), int(b))
        return botcolor

    async def devs():
        devs = []
        return devs

    def cog_check(self, ctx):
        if self.client.is_owner(ctx.author):
            return True
        elif ctx.author.id in Config.devs():
            return True
        else:
            return False

def setup(client):
    client.add_cog(Config(client))
