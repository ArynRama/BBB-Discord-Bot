import json
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
    prefixes = prefixeslist(client, message)
    return commands.when_mentioned_or(*prefixes)(client, message)

 
client = commands.Bot(command_prefix=get_prefix,description=description, intent=intents)

def prefixeslist(client, message):
    if isinstance(message.channel, discord.DMChannel):
        return Config.defaultprefix()
    else:
        with open(r"C:\Users\aryan\Documents\Workspace\Bots\DiscordBot2\json\prefixes.json", "r") as f:
            prefixes = json.load(f)
        guild = message.guild
        id = guild.id
        if str(id) in prefixes:
            return prefixes[str(id)]
        else:
            prefixes[str(id)] = Config.defaultprefix()
            with open(r"C:\Users\aryan\Documents\Workspace\Bots\DiscordBot2\json\prefixes.json", "w") as f:
                json.dump(prefixes, f)
            return prefixes[str(id)]

@client.event
async def on_ready():
    version = Config.version()
    print(f'Logged in as {client.user} (ID: {client.user.id})')
    print(f'Bot Version: {version}')
    print('Owner: ArynRama#6043')
    print('------')

@client.check
async def blacklisted(ctx):
    with open(r"C:\Users\aryan\Documents\Workspace\Bots\DiscordBot2\json\bl_channels.json", "r") as f:
        channels = json.load(f)
    with open(r"C:\Users\aryan\Documents\Workspace\Bots\DiscordBot2\json\bl_users.json", "r") as e:
        ids = json.load(e)
    if str(ctx.channel.id) in channels:
        embed = discord.Embed(
            title=f"This Channel is blacklisted", color=Config.botcolor())
        await ctx.send(embed=embed, delete_after=5)
        raise Blacklisted_Channel("Blacklisted.")
    else:
        if str(ctx.author.id) in ids:
            with open(r"C:\Users\aryan\Documents\Workspace\Bots\DiscordBot2\json\bl_users.json", "r") as e:
                ids = json.load(e)
                reason = ids[str(ctx.author.id)]
            embed = discord.Embed(
                title=f"{ctx.author} is blacklisted for {reason}", color=Config.botcolor())
            await ctx.send(embed=embed, delete_after=10)
            raise Blacklisted_User("Blacklisted.")
        else:
            return True

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

client.run(Config.token())
