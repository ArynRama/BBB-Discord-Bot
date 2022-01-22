import discord
from discord.ext import commands
from discord import FFmpegPCMAudio
from discord.player import FFmpegAudio


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
            await ctx.send(f"Joining {channel.name}", delete_after=5)
            voice.stop
        else:
            await ctx.send("You must be connected to a voice channel.", delete_after=5)

    @commands.command(pass_context=True)
    async def leave(self, ctx):
        """Makes the bot leave the voice channel."""
        if ctx.voice_client:
            await ctx.guild.voice_client.disconnect()
            await ctx.send("Disconnected.", delete_after=5)
        else:
            await ctx.send("I am not connected to a voice channel.", delete_after=5)

    @commands.command(pass_context=True)
    async def pause(self, ctx):
        """Pauses the music."""
        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        if voice.is_playing:
            await ctx.send("Pausing...", delete_after=5)
            await voice.pause()
        else:
            await ctx.send("Not playing anything.", delete_after=5)

    @commands.command(pass_context=True)
    async def resume(self, ctx):
        """Resumes the music"""
        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        if voice.is_paused:
            await ctx.send("Resuming...", delete_after=5)
            await voice.resume()
        else:
            await ctx.send("Not paused right now.", delete_after=5)

    @commands.command(pass_context=True)
    async def stop(self, ctx):
        """Stops the music."""
        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        await voice.stop()

    @commands.command(pass_context=True)
    async def play(self, ctx, *, args):
        """Plays music."""
        voice = ctx.guild.voice_client
        name = args
        song = "./music/" + name + ".mp3"
        source = FFmpegPCMAudio(song)
        await ctx.send(f"Playing {args}.")
        voice.play(source)

    @commands.command(pass_context=True)
    async def queue(self, ctx, *, args):
        """Queues a song."""
        name = args.lower()
        song = "music/" + name + ".mp3"
        guild_id = ctx.message.guild.id
        if args == "list" or args == "":
            await ctx.send(queues)
        else:
            await ctx.send("Added to queue")
            if guild_id in queues:
                queues[guild_id].append(song)
            else:
                queues[guild_id] = song


def setup(client):
    client.add_cog(Music(client))
