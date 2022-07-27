import os
import json
import signal
import discord
import pyrebase
import tracemalloc
from discord import client
from discord.ext import commands, bridge
from essential.help import HelpCmd
from essential.config import prefix

description = f'''A bot I made for BBB.'''
version = "2.4.0"
intents = discord.Intents.all()
intents.members = True
intents.message_content = True
tracemalloc.start()


class clients(commands.Bot):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

    async def on_ready(self):
        print(f'Logged in as {client.user} (ID: {client.user.id})')
        print(f'Bot Version: {version}')
        print('Owner: ArynRama#6043')
        print(f'Prefix: {prefix()}')
        print('------')

    preConfig = os.getenv("FB_Info")
    firebaseConfig = json.loads(preConfig)

    firebase = pyrebase.initialize_app(firebaseConfig)
    db = firebase.database()

client = clients(command_prefix=commands.when_mentioned_or(prefix()), description=description, intent=intents, help_command=HelpCmd())
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
    try:
        client.wavelink.disconnect()
        print('Shutting Down.')
        exit()
    except:
        print('Shutting Down.')
        exit()

signal.signal(signal.SIGTERM, signal_handler)
print('Shutting Down.')
signal.pause()