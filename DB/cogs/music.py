import typing
import asyncio
import discord
import wavelink
import youtubesearchpython
from discord.ext import commands
from essential.player import Player
from essential.checks import is_dev
from essential.config import botcolor, devs

class Music(commands.Cog):
    def __init__(self, client):
        self.client = client

        self.client.loop.create_task(self.connect_nodes())

    async def cog_check(self, ctx):
        if isinstance(ctx.channel, discord.DMChannel):
            embed = discord.Embed(title="Music commands are not available in DMs.", color=botcolor())
            await ctx.send(embed=embed, delete_after=5)
            return False
        else:
            return True
        
    async def connect_nodes(self):
        """Connect to Lavalink nodes."""
        await self.client.wait_until_ready()

        self.wavelink = await wavelink.NodePool.create_node(bot=self.client, host="lavalink.oops.wtf",port=443,https=True,password="www.freelavalink.ga", identifier="Lavalink")

    @commands.Cog.listener()
    async def on_ready(self):
        print("Music has been loaded.")
    
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if not member.bot and after.channel is None:
            if not [m for m in before.channel.members if not m.bot]:
                pass
    
    @commands.Cog.listener()
    async def on_wavelink_node_ready(self, node):
        print(f"Connected to {node.identifier}")
    
    @commands.Cog.listener()
    async def on_wavelink_track_end(self, Player: wavelink.Player, track: wavelink.Track, reason):
        player = Player
        queue = player.Queue
        if queue.is_empty:
            pass
        else:
            await player.play(queue.get())


    @commands.command(pass_context=True, aliases=["connect", "c", "j"])
    async def join(self, ctx):
        """Makes the bot join the channel you're in"""
        player = Player()
        if ctx.author.voice:
            channel = ctx.author.voice.channel
            await channel.connect(cls=player)
        else:
            embed = discord.Embed(color=botcolor(), title=f"You must be connected to a voice channel.")
            await ctx.send(embed = embed, delete_after=5)

    @commands.command(pass_context=True, aliases=["forceconnect", "fc", "fj"])
    @is_dev()
    async def forcejoin(self, ctx, *, channel:typing.Optional[discord.VoiceChannel]=None):
        """Makes the bot join the channel you're in"""
        player = Player()
        if channel == None:
            embed = discord.Embed(color=botcolor(), title=f"Please add a valid voice channel to join.")
            await ctx.send(embed = embed, delete_after=5)
        else:
            await channel.connect(cls=player)
            embed = discord.Embed(color=botcolor(), title=f"Joining {channel.name}")
            await ctx.send(embed = embed, delete_after=5)

    @commands.command(pass_context=True, aliases=["disconnect", "dc","away"])
    async def leave(self, ctx):
        """Makes the bot leave the voice channel."""
        player = ctx.voice_client
        if str(ctx.author.id) in devs():
            await player.disconnect()
            embed = discord.Embed(color=botcolor(), title = "Disconnected.")
            await ctx.send(embed = embed, delete_after=5)
        elif ctx.author.voice:
            await player.disconnect()
            embed = discord.Embed(color=botcolor(), title = "Disconnected.")
            await ctx.send(embed = embed, delete_after=5)
        else:
            embed = discord.Embed(color=botcolor(), title = "You are not in the voice channel.")
            await ctx.send(embed = embed, delete_after=5)
 
    @commands.command(pass_context=True, aliases=["p", "sing"])
    async def play(self, ctx, *, search:wavelink.YouTubeTrack= None):
        """Plays music."""
        if search == None:
            embed = discord.Embed(title="You must include a song.",color=botcolor())
            return await ctx.send(embed=embed, delete_after=5)
        if ctx.author.voice or ctx.author.id in devs():
            if ctx.voice_client:
                player = ctx.voice_client
                if player.is_playing:
                    player.Queue.put(search)
                else:
                    await player.play(search)
            else:
                player = Player()
                channel = ctx.message.author.voice.channel
                await channel.connect(cls=player)
                player = ctx.voice_client
                await player.play(search)
        else:
            embed = discord.Embed(color=botcolor(), title = "You must be connected to a voice channel.")
            await ctx.send(embed = embed, delete_after=5)
        
    @commands.command(pass_context=True, aliases=["pn", "addfrontqueue"])
    async def playnext(self, ctx, *, search:wavelink.YouTubeTrack= None):
        """Adds music to the queue."""
        if search == None:
            embed = discord.Embed(title="You must include a song.",color=botcolor())
            return await ctx.send(embed=embed, delete_after=5)
        if ctx.author.voice or ctx.author in devs():
            if ctx.voice_client:
                player = ctx.voice_client
                if ctx.voice_client.is_playing:
                    queue = player.Queue
                    queue.put_at_front(search)
                else:
                    await player.play(search)
            else:
                player = Player()
                channel = ctx.message.author.voice.channel
                await channel.connect(cls=player)
                player = ctx.voice_client
                await player.play(search)
        else:
            embed = discord.Embed(color=botcolor(), title = "You must be connected to a voice channel.")
            await ctx.send(embed = embed, delete_after=5)

    @commands.command(pass_context=True, aliases=["rest", "wait"])
    async def pause(self, ctx):
        """Pauses the music."""
        player = ctx.voice_client
        if ctx.author.voice or ctx.author.id in devs():
            if player.is_playing:
                embed = discord.Embed(color=botcolor(), title = "Pausing...")
                await ctx.send(embed = embed, delete_after=5)
                await player.pause()
            else:
                embed = discord.Embed(color=botcolor(), title="Not playing anything.")
                await ctx.send(embed = embed, delete_after=5)
        else:
            embed = discord.Embed(color=botcolor(), title=f"You must be connected to {ctx.voice_client.channel}.")
            await ctx.send(embed = embed, delete_after=5)

    @commands.command(pass_context=True)
    async def resume(self, ctx):
        """Resumes the music"""
        if ctx.author.voice or ctx.author.id in devs():
            player = ctx.voice_client
            if player.is_paused:
                embed = discord.Embed(color=botcolor(), title = "Resuming...")
                await ctx.send(embed = embed, delete_after=5)
                await player.resume()
            else:
                embed = discord.Embed(color=botcolor(), title = "Not paused right now.")
                await ctx.send(embed = embed, delete_after=5)
        else:
            embed = discord.Embed(color=botcolor(), title = f"You must be connected to {ctx.voice_client.channel}.")
            await ctx.send(embed = embed, delete_after=5)

    @commands.command(pass_context=True)
    async def stop(self, ctx):
        """Stops the music."""
        if ctx.author.voice or ctx.author.id in devs():
            player = ctx.voice_client
            if player.is_playing() or player.is_paused():
                embed = discord.Embed(color=botcolor(), title = "Stoping.")
                await ctx.send(embed = embed, delete_after=5)
                await player.stop()
            else:
                embed = discord.Embed(color=botcolor(), title = "Not playing anything")
                await ctx.send(embed = embed, delete_after=5)
        else:
            embed = discord.Embed(color=botcolor(), title=f"You must be connected to {ctx.voice_client.channel}.")
            await ctx.send(embed=embed, delete_after=5)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
    
        if not member.id == self.client.user.id:
            return
        elif before.channel is None:
            voice = after.channel.guild.voice_client
            time = 0
            while True:
                await asyncio.sleep(1)
                time = time + 1
                if voice.is_playing() and not voice.is_paused():
                    time = 0
                if time == 600:
                    await voice.disconnect()
                if not voice.is_connected():
                    break

    @commands.command(pass_context=True)
    async def queue(self, ctx):
        """View the queue."""
        queue = ctx.voice_client.Queue
        if isinstance(queue, wavelink.Queue):
            if queue.is_empty:
                embed = discord.Embed(color=botcolor(), title="No songs currently queued.")
                await ctx.send(embed=embed, delete_after= 5)
            else:
                embed = discord.Embed(color=botcolor(), title="Queue")
                i = 0
                for a in queue:
                    a = str(a)
                    i = i + 1
                    link = youtubesearchpython.VideosSearch(a,limit=1).result()["result"][0]["link"]
                    embed.add_field(name=f"**#{i}**  {a}" , value = f"{link}", inline=False)
                await ctx.send(embed=embed, delete_after= 30)
        else:
            embed = discord.Embed(color=botcolor(), title="No songs currently queued.")
            await ctx.send(embed=embed, delete_after= 5)
    
    @commands.command(pass_context=True)
    async def skip(self, ctx):
        """Skip this song."""
        if ctx.author.voice:
            if ctx.voice_client:
                player = ctx.voice_client
                queue = player.Queue
                if queue.is_empty:
                    await player.stop()
                    embed = discord.Embed(color=botcolor(),title=f"Stoping.")
                else:
                    await player.stop()
                    embed = discord.Embed(color=botcolor(),title=f"Skipping.")
                await ctx.send(embed=embed, delete_after=5)
            else:
                embed = discord.Embed(color=botcolor(),title=f"Not playing anything.")
                await ctx.send(embed=embed, delete_after=5)
        else:
            embed = discord.Embed(color=botcolor(), title="You must be connected to a voice channel.")
            await ctx.send(embed=embed, delete_after=5)

def setup(client):
    client.add_cog(Music(client))
