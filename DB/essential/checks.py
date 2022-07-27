import discord
from discord.ext import commands, bridge
from essential.config import devs
from essential.errors import NotDev

def is_dev():
    def predicate(ctx: bridge.BridgeContext):
        try:
            if str(ctx.author.id) in devs():
                return True
        except:
            raise NotDev()
    
    return commands.check(predicate)
