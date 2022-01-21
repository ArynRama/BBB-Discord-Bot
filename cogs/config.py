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

    def version():
        version = Config.config['Bot']['Version']
        return version

    def botcolor():
        botcolors = Config.config['Chat']['BotColor'].split(", ")
        r = botcolors[0]
        g = botcolors[1]
        b = botcolors[2]
        botcolor = Color.from_rgb(int(r),int(g),int(b))
        return botcolor


def setup(client):
    client.add_cog(Config(client))
