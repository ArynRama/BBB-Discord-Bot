import discord
from essential.config import botcolor
from discord.ext import commands

hidden_cogs = ('Config','Events')
class HelpCmd(commands.HelpCommand):
    def __init__(self):
        super().__init__()
        
    async def send_bot_help(self, mapping):
        mapping.pop(None)
        channel = self.get_destination()
        coglist = sorted(
            [cog.qualified_name for cog in mapping if cog.qualified_name not in hidden_cogs])
        coglist = await self.filter_commands(coglist)
        description = f'**Prefix is `-`**\nThere are {len(coglist)} modules'
        lines = '\n'.join(coglist)
        cogs = f"```prolog\n{lines}```"

        emb = discord.Embed(title="RTFM help menu (online version)", colour=botcolor(), description=description)
        emb.add_field(name="Modules", value=cogs)
        emb.set_footer(text="Type do help <module> to see commands or do help <command>")

        await channel.send(embed=emb)
    
    async def send_cog_help(self, cog):
        if cog.qualified_name in hidden_cogs:
            return await self.get_destination().send(f'No command or cog called "{cog.qualified_name}" found. Remember names are case-sensitive.')
        commandsList = await self.filter_commands(cog.get_commands())

        emb = discord.Embed(title=f"Commands from {cog.qualified_name} module (online version)", colour=botcolor())

        emb.set_footer(
            text="<argument needed> [optional argument] [a|b] : either a or b")

        for command in commandsList:
            doc = command.short_doc
            if command.clean_params or command.aliases:
                if command.brief:
                    signature = command.help.split('\n')[0]
                else:
                    signature = f'{command.qualified_name} {command.signature}'
                doc += f'\n**Usage -** -{signature}'

            emb.add_field(name=command.name, value=doc, inline=False)

        await self.get_destination().send(embed=emb)

    
    async def send_command_help(self, command):
        if command.hidden or command.cog.qualified_name in hidden_cogs:
            return await self.get_destination().send(f'No command or cog called "{command.qualified_name}" found. Remember names are case-sensitive.')

        description = command.help
        if not description.startswith(command.qualified_name):
            description = f"{command.qualified_name} {command.signature}\n\n{description}"

        emb = discord.Embed(title=f"Help for command {command.qualified_name}", colour=botcolor())

        await self.get_destination().send(embed=emb)

    async def send_group_help(self, group):
        subcommands = group.commands
        if len(subcommands) == 0:
            return await self.send_command_help(group)

        entries = await self.filter_commands(subcommands, sort=True)
        await self.get_destination().send("Not finished.")
