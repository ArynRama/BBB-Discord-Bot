import os
import json
import signal
import discord
import pyrebase
import tracemalloc
from discord import client
from discord.ext import commands, bridge
from essential.config import prefix
from essential.help import HelpCmd

description = f'''A bot I made for BBB.'''
version = "2.4.0"
intents = discord.Intents.all()
tracemalloc.start()

class clients(bridge.Bot):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

    async def on_ready(self):
        print(f'Logged in as {client.user} (ID: {client.user.id})')
        print(f'Bot Version: {version}')
        print('Owner: ArynRama#6043')
        print('------')
        print(f'Prefix: -')

    preConfig = os.getenv("FB_Info")
    firebaseConfig = json.loads(preConfig)

    command_prefix='-'

    firebase = pyrebase.initialize_app(firebaseConfig)
    db = firebase.database()

client = clients(description=description, intent=intents, help_command=HelpCmd())

class LoadCogs:

    extentions = [
        "music",
        "miscellaneous",
        "management"
    ]
    dependencies = [
        "event",
        "dev"
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

client.run(str(os.getenv("token")))

def signal_handler(sig, frame):
    print('Disconnecting Wavelink.')
    client.wavelink.disconnect()
    print('Shutting Down.')
    exit()

signal.signal(signal.SIGTERM, signal_handler)
print('Shutting Down.')
signal.pause()