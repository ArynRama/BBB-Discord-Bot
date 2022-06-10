import os
import dotenv
import discord
import tracemalloc
from discord import client
from discord.ext import commands
from essential.help import HelpCmd

description = f'''A bot I made for BBB.'''
version = "2.0.0beta"
intents = discord.Intents.all()
tracemalloc.start()
dotenv.load_dotenv()
class clients(commands.Bot):
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

    async def on_ready(self):
        print(f'Logged in as {client.user} (ID: {client.user.id})')
        print(f'Bot Version: {version}')
        print('Owner: ArynRama#6043')
        print('------')
client = clients(command_prefix="-",description=description, intent=intents, help_command=HelpCmd())

class LoadCogs:
    extentions = [
        "music",
        "mischief"
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