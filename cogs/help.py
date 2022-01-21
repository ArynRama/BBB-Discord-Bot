import discord
from main import client
from cogs.config import Config
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, client):
        self.client = client

    class HelpCmd(commands.HelpCommand):
        def __init__(self):
            super().__init__()
        
        async def send_bot_help(self, mapping):
            channel = self.get_destination()
            embed = discord.Embed(title="Help",color=Config.botcolor())
            commands = ""
            for cog in mapping:
                for command in cog.get_commands():
                    commands += f"{command} "
                await channel.send(commands)
                commands = ""
            #await channel.send(embed = embed)
        
        async def send_cog_help(self, cog):
            return await super().send_cog_help(cog)
        
        async def send_command_help(self, command):
            return await super().send_command_help(command)

        async def send_group_help(self, group):
            return await super().send_group_help(group)
    
    client.help_command = HelpCmd()
def setup(client):
    client.add_cog(Help(client))