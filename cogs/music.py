import discord
import youtube_dl
from cogs.config import Config
from discord.ext import commands
from youtubesearchpython import VideosSearch

queue = {}

async def check_queue(ctx, id):  
    if str(id) in queue.keys():
        link = queue[str(id)].pop()
        YDL_OPTIONS = {'format':"bestaudio"}
        FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options':'-vn'}
        with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(link, download=False)
            url2 = info['formats'][0]['url']
            source = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS)
            ctx.guild.voice_client.play(source)

class Music(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Music has been loaded.")

    @commands.command(pass_context=True)
    async def join(self, ctx, member:discord.Member=None):
        """Makes the bot join the channel you're in"""
        if ctx.author.voice:
            channel = ctx.message.author.voice.channel
            voice = await channel.connect()
            embed = discord.Embed(color=Config.botcolor(), title=f"Joining {channel.name}")
            await ctx.send(embed = embed, delete_after=5)
            voice.stop
        else:
            embed = discord.Embed(color=Config.botcolor(), title = "You must be connected to a voice channel.")
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
        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        if voice.is_paused:
            embed = discord.Embed(color=Config.botcolor(), title = "Resuming...")
            await ctx.send(embed = embed, delete_after=5)
            await voice.resume()
        else:
            embed = discord.Embed(color=Config.botcolor(), title = "Not paused right now.")
            await ctx.send(embed = embed, delete_after=5)

    @commands.command(pass_context=True)
    async def stop(self, ctx):
        """Stops the music."""
        embed = discord.Embed(color=Config.botcolor(), title = "Stoping.")
        await ctx.send(embed = embed, delete_after=5)
        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        await voice.pause()

    @commands.command(pass_context=True)
    async def play(self, ctx, *, args):
        """Plays music."""
        voice = ctx.guild.voice_client
        if voice.is_connected():
            if voice.is_playing():
                embed = discord.Embed(color=Config.botcolor(), title="Added to queue.")
                await ctx.send(embed=embed,delete_after=5)
                search = VideosSearch(args, limit=1)
                result = search.result()
                song = result['result'][0]['title']
                img = result['result'][0]['thumbnails'][0]['url']
                link = result['result'][0]['link']
                if len(queue.keys())==0:
                    queue[str(ctx.guild.id)] = {link}
                else:
                    if queue[str(ctx.guild.id)] == {}:
                        queue[str(ctx.guild.id)] = {link}
                    else:
                        queue[str(ctx.guild.id)].add(link)
            else:
                YDL_OPTIONS = {'format':"bestaudio"}
                FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options':'-vn'}
                search = VideosSearch(args, limit =1)
                result = search.result()
                song = result['result'][0]['title']
                img = result['result'][0]['thumbnails'][0]['url']
                if not(args.__contains__("youtube.com") or args.__contains__("youtu.be")):
                    with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
                        link = result['result'][0]['link']
                        info = ydl.extract_info(link, download=False)
                else:
                    with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
                        info = ydl.extract_info(args,download=False)
                        link = args
                url2 = info['formats'][0]['url']
                source = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS)
                await voice.play(source, after=lambda x=None: check_queue(ctx, str(ctx.message.guild.id)))
                embed = discord.Embed(color=Config.botcolor(), title = f"Playing {song}.")
                await ctx.send(embed=embed,delete_after=5)
        else: 
            embed = discord.Embed(color=Config.botcolor(),title="Not connected to a voice channel.")
            await ctx.send(embed=embed,delete_after = 5)

    @commands.command(pass_context=True)
    async def queue(self, ctx, *, args):
        """View the queue."""
        guild_id = str(ctx.message.guild.id)
        i = 1
        for a in queue[guild_id]:
            embed = discord.Embed(color=Config.botcolor(), title="Queue")
            embed.add_field(name = i,value = a)
            i = i+1
        await ctx.send(embed=embed, delete_after= 30)


def setup(client):
    client.add_cog(Music(client))
