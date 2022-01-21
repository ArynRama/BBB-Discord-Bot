from configparser import ConfigParser
from discord import Color
from discord.ext import commands

class Config(commands.Cog):
    def __init__(self, client):
        self.client = client

    config = ConfigParser()
    config.read("options.ini")
    
    def desc():
        desc = Config.config['Bot']['Description']
        return desc

    def token():
        token = Config.config['Bot']['Token']
        return token

    def version():
        version = Config.config['Bot']['Version']
        return version

    def defaultprefix():
        defaultprefix = Config.config['Chat']['CommandPrefix']
        return defaultprefix

    def botcolor():
        botcolors = Config.config['Chat']['BotColor'].split(", ")
        r = botcolors[0]
        g = botcolors[1]
        b = botcolors[2]
        botcolor = Color.from_rgb(int(r),int(g),int(b))
        return botcolor

    async def devs():
        devs = Config.config['Permissions']['DevIDs'].split(", ")
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
