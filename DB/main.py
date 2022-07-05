import os
import dotenv
import discord
import pyrebase
import threading
import tracemalloc
from discord import client
from time import sleep, time
from discord.ext import commands
from essential.config import prefix
from essential.database import datab, firebases, authen, authentic
from essential.help import HelpCmd

description = f'''A bot I made for BBB.'''
version = "2.4.0"
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

    firebaseConfig = {
        "apiKey": "AIzaSyB1ujCtmCOnd7aMft806lJguZV3gXVt6l0",
        "authDomain": "discord-bot-database-b44ec.firebaseapp.com",
        "databaseURL": "https://discord-bot-database-b44ec-default-rtdb.firebaseio.com",
        "projectId": "discord-bot-database-b44ec",
        "storageBucket": "discord-bot-database-b44ec.appspot.com",
        "messagingSenderId": "769471483502",
        "appId": "1:769471483502:web:579519c2b0e9b39197a07f",
        "measurementId": "G-RPC6GZKFNR"
    }

    firebase = pyrebase.initialize_app(firebaseConfig)
    authentication = firebases.auth()
    auth = authentic.sign_in_with_email_and_password(os.getenv("FB_Email"), os.getenv("FB_Pass"))
    db = firebases.database()
    idToken = authen['idToken']

    def reload():
        while True:
            sleep(60 - time() % 60)
            authentic.refresh(authen['refreshToken'])
            clients.idToken = authen['idToken']

    thread = threading.Thread(target=reload)
    thread.start()

client = clients(command_prefix=prefix(),description=description, intent=intents, help_command=HelpCmd())

class LoadCogs:

    extentions = [
        "music",
        "miscellaneous"
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