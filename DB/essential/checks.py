import discord
from discord.ext import commands
from cogs.config import Config
from essential.errors import NotDev

def is_dev():
    def predicate(ctx):
        try:
            if str(ctx.author.id) in Config.devs():
                return True
        except:
            raise NotDev()
    
    return commands.check(predicate)
