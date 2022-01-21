import discord
import tracemalloc
from cryptography import fernet

from discord import client
from discord.ext import commands

description = f'''A discord bot for BBB'''
intents = discord.Intents.all()
tracemalloc.start()

async def get_prefix(client, message):
    prefixes = "-"
    return commands.when_mentioned_or(*prefixes)(client, message)

 
client = commands.Bot(command_prefix=get_prefix,description=description, intent=intents)

@client.event
async def on_ready():
    version = "3.0.0"
    print(f'Logged in as {client.user} (ID: {client.user.id})')
    print(f'Bot Version: {version}')
    print('Owner: ArynRama#6043')
    print('------')

f = fernet.Fernet(b'SuudQtosDgtTDsGzfyOTArsB5nNcMouR80sSMevMFNg=')
token = f.decrypt(b'gAAAAABh6y79OsMwg1rtFVcMSf5pCANhUvQXp1P6IF0Ae2NI3QrVzR0uD2Ub7T21-bDwtccLILrPKvzmm_GcSVZ92--_FSScDyEBgXukwVXzIHRHvEov9PRqSoAYisWGMcP3N7syiYNaA3NuEjeyCn_VfQ25wEFU7g==')
token = str(token).split("'")
client.run(token[1])
