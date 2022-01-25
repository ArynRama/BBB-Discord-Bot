import discord
import youtube_dl
from cogs.config import Config
from discord.ext import commands
from discord import FFmpegPCMAudio

queues = {}

def check_queue(ctx, id):
    if queues[id] != {}:
        ctx.send(id)
        voice = ctx.guild.voice_client
        song = queues[id].pop(0)
        source = FFmpegPCMAudio(song)
        player = voice.play(source)


class Music(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Music has been loaded.")

    @commands.command(pass_context=True)
    async def join(self, ctx):
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
        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        await voice.pause()
        embed = discord.Embed(color=Config.botcolor(), title = "Stoping.")
        await ctx.send(embed = embed, delete_after=5)

    @commands.command(pass_context=True)
    async def play(self, ctx, *, url):
        """Plays music."""
        voice = ctx.guild.voice_client
        YDL_OPTIONS = {'format':"bestaudio"}
        FFMPEG_OPTIONS = {'beforeoptions': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options':'-vn'}

        with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download = False)
            url2 = info['formats'][0]['url']
            source = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS)
            voice.play(source)
            embed = discord.Embed(color=Config.botcolor(), title = f"Playing {url}.")
            await ctx.send(embed=embed,delete_after=5)

    @commands.command(pass_context=True)
    async def queue(self, ctx, *, args):
        """Queues a song."""
        name = args.lower()
        song = "music/" + name + ".mp3"
        guild_id = ctx.message.guild.id
        if args == "":
            await ctx.send(queues)
        else:
            embed = discord.Embed(color=Config.botcolor(), title = "Added to queue.")
            await ctx.send(embed = embed, delete_after = 5)
            if guild_id in queues:
                queues[guild_id].append(song)
            else:
                queues[guild_id] = song


def setup(client):
    client.add_cog(Music(client))
