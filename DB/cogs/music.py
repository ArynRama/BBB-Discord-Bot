from turtle import title
import typing
import wave
import discord
import wavelink
import youtube_dl
from cogs.config import Config
from essential.checks import is_dev
from discord.ext import commands
from youtubesearchpython import VideosSearch
from essential.player import Player

class Music(commands.Cog, wavelink.WavelinkMixin):
    def __init__(self, client):
        self.client = client
        self.wavelink = wavelink.Client(bot=client)
        self.client.loop.create_task(self.start_nodes())

    async def cog_check(self, ctx):
        if isinstance(ctx.channel, discord.DMChannel):
            embed = discord.Embed(title="Music commands are not available in DMs.", color=Config.botcolor())
            await ctx.send(embed=embed, delete_after=5)
            return False
        else:
            return True
        
    async def start_nodes(self):
        await self.client.wait_until_ready()
        await self.wavelink.initiate_node(host="lavalink.oops.wtf",region="us_central", rest_uri="lavalink.oops.wtf",port=443,identifier="Lavalink",secure=True,password="www.freelavalink.ga")

    def get_player(self, obj):
        if isinstance(obj, commands.Context):
            return self.wavelink.get_player(obj.guild.id, cls=Player, context=obj)
        elif isinstance(obj, discord.Guild):
            return self.wavelink.get_player(obj.id, cls=Player)

    @commands.Cog.listener()
    async def on_ready(self):
        print("Music has been loaded.")
    
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if not member.bot and after.channel is None:
            if not [m for m in before.channel.members if not m.bot]:
                pass
    
    @wavelink.WavelinkMixin.listener()
    async def on_node_ready(self, node):
        print(f"Connected to {node.identifier}")

    @commands.command(pass_context=True, aliases=["connect", "c", "j"])
    async def join(self, ctx):
        """Makes the bot join the channel you're in"""
        player = self.get_player(ctx)
        if ctx.author.voice:
            channel_c = ctx.author.voice.channel
            await player.connect(channel_c.id)
        else:
            embed = discord.Embed(color=Config.botcolor(), title=f"You must be connected to a voice channel.")
            await ctx.send(embed = embed, delete_after=5)

    @commands.command(pass_context=True, aliases=["forceconnect", "fc", "fj"])
    @is_dev()
    async def forcejoin(self, ctx, *, channel:typing.Optional[discord.VoiceChannel]=None):
        """Makes the bot join the channel you're in"""
        player = self.get_player(ctx)
        if channel == None:
            embed = discord.Embed(color=Config.botcolor(), title=f"Please add a valid voice channel to join.")
            await ctx.send(embed = embed, delete_after=5)
        else:
            await player.connect(channel.id)
            embed = discord.Embed(color=Config.botcolor(), title=f"Joining {channel.name}")
            await ctx.send(embed = embed, delete_after=5)

    @commands.command(pass_context=True)
    async def leave(self, ctx):
        """Makes the bot leave the voice channel."""
        if ctx.voice_client:
            await ctx.guild.voice_client.disconnect()
            embed = discord.Embed(color=Config.botcolor(), title = "Disconnected.")
            await ctx.send(embed = embed, delete_after=5)
        else:
            embed = discord.Embed(color=Config.botcolor(), title = "I am not connected to a voice channel.")
            await ctx.send(embed = embed, delete_after=5)

    @commands.command(pass_context=True)
    async def pause(self, ctx):
        """Pauses the music."""
        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        if voice.is_playing:
            embed = discord.Embed(color=Config.botcolor(), title = "Pausing...")
            await ctx.send(embed = embed, delete_after=5)
            await voice.pause()
        else:
            embed = discord.Embed(color=Config.botcolor(), title="Not playing anything.")
            await ctx.send(embed = embed, delete_after=5)

    @commands.command(pass_context=True)
    async def resume(self, ctx):
        """Resumes the music"""
        if ctx.author.voice:
            voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
            if voice.is_paused:
                embed = discord.Embed(color=Config.botcolor(), title = "Resuming...")
                await ctx.send(embed = embed, delete_after=5)
                await voice.resume()
            else:
                embed = discord.Embed(color=Config.botcolor(), title = "Not paused right now.")
                await ctx.send(embed = embed, delete_after=5)
        else:
            embed = discord.Embed(color=Config.botcolor(), title = "You must be connected to a voice channel.")
            await ctx.send(embed = embed, delete_after=5)

    # @commands.command(pass_context=True)
    # async def stop(self, ctx):
    #     """Stops the music."""
    #     if ctx.author.voice:
    #         voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
    #         if voice.is_playing() or voice.is_paused():
    #             embed = discord.Embed(color=Config.botcolor(), title = "Stoping.")
    #             await ctx.send(embed = embed, delete_after=5)
    #             # queue[str(ctx.guild.id)] = [{}]
    #             await voice.stop()
    #         else:
    #             embed = discord.Embed(color=Config.botcolor(), title = "Not playing anything")
    #             await ctx.send(embed = embed, delete_after=5)
    #     else:
    #         embed = discord.Embed(color=Config.botcolor(
    #         ), title="You must be connected to a voice channel.")
    #         await ctx.send(embed=embed, delete_after=5)

    # @commands.command(pass_context=True)
    # async def play(self, ctx, *, args= None):
    #     """Plays music."""
    #     if args == None:
    #         embed = discord.Embed(title="You must include a song.",color=Config.botcolor())
    #         return await ctx.send(embed=embed, delete_after=5)
    #     if ctx.author.voice:
    #         voice_client = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
    #         if voice_client == None:
    #             channel = ctx.message.author.voice.channel
    #             voice = await channel.connect()
    #             embed = discord.Embed(color=Config.botcolor(), title=f"Joining {channel.name}")
    #             await ctx.send(embed = embed, delete_after=5)
    #             voice.stop
    #         voice = ctx.guild.voice_client
    #         YDL_OPTIONS = {'format': "bestaudio"}
    #         FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    #         search = VideosSearch(args, limit=1)
    #         result = search.result()
    #         title = result['result'][0]['title']
    #         link = result['result'][0]['link']
    #         if args.__contains__("youtube.com") or args.__contains__("youtu.be"):
    #             with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
    #                 info = ydl.extract_info(args, download=False)
    #         else:
    #             with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
    #                 link = result['result'][0]['link']
    #                 info = ydl.extract_info(link, download=False)
    #         url2 = info['formats'][0]['url']
    #         if voice.is_playing():
    #             embed = discord.Embed(color=Config.botcolor(), title=f"Added {title} queue.", description = link)
    #             await ctx.send(embed=embed, delete_after=5)
    #             if len(queue.keys()) == 0:
    #                 queue[str(ctx.guild.id)] = [{"title": title, "link": link, "url2": url2}]
    #             else:
    #                 if len(queue[str(ctx.guild.id)]) >= 1:
    #                     queue[str(ctx.guild.id)].append({"title": title, "link": link, "url2": url2})
    #                 elif queue[str(ctx.guild.id)] == [] or queue[str(ctx.guild.id)] == {}:
    #                     queue[str(ctx.guild.id)] = [{"title": title, "link": link, "url2": url2}] 
    #         else:
    #             source = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS)
    #             voice.play(source, after=lambda x=None: check_queue(ctx))
    #             embed = discord.Embed(color=Config.botcolor(), title=f"Playing {title}.", description=link)
    #             await ctx.send(embed=embed, delete_after=5)
    #     else:
    #         embed = discord.Embed(color=Config.botcolor(), title = "You must be connected to a voice channel.")
    #         await ctx.send(embed = embed, delete_after=5)

    # @commands.command(pass_context=True)
    # async def queue(self, ctx):
    #     """View the queue."""
    #     guild_id = str(ctx.message.guild.id)
    #     i = 1
    #     embed = discord.Embed(color=Config.botcolor(), title="Queue")
    #     for a in queue[guild_id]:
    #         embed.add_field(name = f"#{i}",value = f"[{a['title']}]({a['link']})", inline=False)
    #         i = i+1
    #     await ctx.send(embed=embed, delete_after= 30)
    
    @commands.command(pass_context=True)
    async def skip(self, ctx):
        """Skip this song."""
        if ctx.author.voice:
            embed = discord.Embed(color=Config.botcolor(),title=f"Skipping.")
            voice = discord.utils.get(ctx.bot.voice_clients, guild = ctx.guild)
            await ctx.send(embed=embed, delete_after=5)
            self.check_queue(ctx)
        else:
            embed = discord.Embed(color=Config.botcolor(), title="You must be connected to a voice channel.")
            await ctx.send(embed=embed, delete_after=5)

def setup(client):
    client.add_cog(Music(client))
