import discord
import tracemalloc

from discord import client
from cogs.config import Config
from discord.ext import commands, ipc
from cryptography import fernet

from cogs.help import HelpCmd

description = f'''{Config.desc()}'''
intents = discord.Intents.all()
tracemalloc.start()
class clients(commands.Bot):
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.ipc = ipc.Server(self,secret_key = "ArynRama25")

    async def on_ready(self):
        version = Config.version()
        print(f'Logged in as {client.user} (ID: {client.user.id})')
        print(f'Bot Version: {version}')
        print('Owner: ArynRama#6043')
        print('------')

    async def on_ipc_ready(self):
        print("Ipc server is ready.")
    
    async def on_ipc_error(self, endpoint, error):
        print(endpoint, "raised", error)
    

client = clients(command_prefix="-",description=description, intent=intents, help_command=HelpCmd())

@client.ipc.route()
async def get_guild_count(data):
    return len(client.guilds)


@client.ipc.route()
async def get_guild_id(data):
    final = []
    for guild in client.guilds:
        final.append(guild.id)
    return final


class LoadCogs:
    extentions = [
        "music",
        "mischief"
    ]
    dependencies = [
        "config",
        "event",
        "owner"
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

client.ipc.start()
client.run(token[1])
