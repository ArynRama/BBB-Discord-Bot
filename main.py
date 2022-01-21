import os
import discord
import tracemalloc

from discord import client
from discord.ext import commands
from boto.s3.connection import S3Connection

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

client.run(input("Bot Token."))
