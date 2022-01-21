import os
import discord
import tracemalloc

from discord import client
from cogs.config import Config
from discord.ext import commands
from cogs.errors import Blacklisted_Channel, Blacklisted_User

description = f'''{Config.desc}'''
intents = discord.Intents.all()
tracemalloc.start()

async def get_prefix(client, message):
    prefixes = "-"
    return commands.when_mentioned_or(*prefixes)(client, message)

 
client = commands.Bot(command_prefix=get_prefix,description=description, intent=intents)

@client.event
async def on_ready():
    version = Config.version()
    print(f'Logged in as {client.user} (ID: {client.user.id})')
    print(f'Bot Version: {version}')
    print('Owner: ArynRama#6043')
    print('------')
class LoadCogs:
    extentions = [
        "management",
        "mischief",
        "dms"
    ]
    dependencies = [
        "dev",
        "errors",
        "events",
        "config",
        "help"
    ]

    loaded_ext = []
    print("Loading dependencies...")
    for ext in dependencies:
        try:
            client.load_extension(f"cogs.{ext.lower()}")
            loaded_ext.append(loaded_ext)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load dependencie {}\n{}'.format(
            ext, exc))
            print(ext)
            exit()

    print("------")
    print("Loading extensions...")
    
    for ext in extentions:
        try:

            client.load_extension(f"cogs.{ext.lower()}")
            loaded_ext.append(loaded_ext)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(
                ext, exc))
    print("------")

client.run(os.environ("token"))
