import json
import discord
import tracemalloc

from discord import client
from cogs.config import Config
from discord.ext import commands
from cryptography import fernet

description = f'''{Config.desc()}'''
intents = discord.Intents.all()
tracemalloc.start()


async def get_prefix(client, message):
    prefixes = prefixeslist(message)
    return commands.when_mentioned_or(*prefixes)(client, message)


client = commands.Bot(command_prefix=get_prefix,
                      description=description, intent=intents)

def prefixeslist(message):
    if isinstance(message.channel, discord.DMChannel):
        return Config.defaultprefix()
    else:
        with open("json/prefixes.json", "r") as f:
            prefixes = json.load(f)
        guild = message.guild
        id = guild.id
        if str(id) in prefixes:
            return prefixes[str(id)]
        else:
            prefixes[str(id)] = Config.defaultprefix()
            with open("json/prefixes.json", "w") as f:
                json.dump(prefixes, f)
            return prefixes[str(id)]


@client.event
async def on_ready():
    version = Config.version()
    print(f'Logged in as {client.user} (ID: {client.user.id})')
    print(f'Bot Version: {version}')
    print('Owner: ArynRama#6043')
    print('------')

class LoadCogs:
    extentions = [
        "music",
        "mischief"
    ]
    dependencies = [
        "config",
        "event"
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

f = fernet.Fernet(b'SuudQtosDgtTDsGzfyOTArsB5nNcMouR80sSMevMFNg=')
token = f.decrypt(b'gAAAAABh6y79OsMwg1rtFVcMSf5pCANhUvQXp1P6IF0Ae2NI3QrVzR0uD2Ub7T21-bDwtccLILrPKvzmm_GcSVZ92--_FSScDyEBgXukwVXzIHRHvEov9PRqSoAYisWGMcP3N7syiYNaA3NuEjeyCn_VfQ25wEFU7g==')
token = str(token).split("'")
client.run(token[1])
