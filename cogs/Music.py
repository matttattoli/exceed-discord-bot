import asyncio
from cogs.utils.checks import *
import discord
import datetime
import youtube_dl

from discord.ext import commands

# Suppress noise about console usage from errors
youtube_dl.utils.bug_reports_message = lambda: ''


ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': 'musicdl/%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'  # ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'before_options': '-nostdin',
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')
        self.duration = data.get('duration')

    @classmethod
    async def from_url(cls, url, *, loop=None):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, ytdl.extract_info, url)

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


class Music:
    def __init__(self, bot):
        self.bot = bot
        self.songqueue = []
        self._currentsong = ''
        self._duration = 0
        self.audio_player = self.bot.loop.create_task(self.queuehandler())
        self.skips = []

    @commands.command()
    async def join(self, ctx, *, channel: discord.VoiceChannel):
        """Joins a voice channel"""

        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)

        await channel.connect()

    # @commands.command()
    # async def play(self, ctx, *, query):
    #     """Plays a file from the local filesystem"""
    #
    #     if ctx.voice_client is None:
    #         if ctx.author.voice.channel:
    #             await ctx.author.voice.channel.connect()
    #         else:
    #             return await ctx.send("Not connected to a voice channel.")
    #
    #     if ctx.voice_client.is_playing():
    #         ctx.voice_client.stop()
    #
    #     source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(query))
    #     ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)
    #
    #     await ctx.send('Now playing: {}'.format(query))

    @commands.command(aliases=['play', 'youtube'])
    async def yt(self, ctx, *, url):
        """Streams from a url (almost anything youtube_dl supports)"""

        if ctx.voice_client is None:
            if ctx.author.voice.channel:
                await ctx.author.voice.channel.connect()
            else:
                return await ctx.send("Not connected to a voice channel.")

        if ctx.voice_client.is_playing():
            ctx.voice_client.stop()

        player = await YTDLSource.from_url(url, loop=self.bot.loop)
        ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)
        self._currentsong = player.title
        self._duration = player.duration
        await ctx.send('Now playing: {}'.format(player.title))

    @commands.group(aliases=['q', 'que'], invoke_without_command=True)
    async def queue(self, ctx, *, url):
        """Adds something to the music queue"""
        if ctx.voice_client is None:
            if ctx.author.voice.channel:
                await ctx.author.voice.channel.connect()
            else:
                return await ctx.send("Not connected to a voice channel.")
        if ctx.voice_client.is_playing() or len(self.songqueue) >= 1:
            player = await YTDLSource.from_url(url, loop=self.bot.loop)
            newsong = {"ctx": ctx, "url": url, "player": player, "name": player.title, "requester": ctx.author}
            self.songqueue.append(newsong)
            return await ctx.send(f"Added `{player.title}` to queue.")
        else:
            player = await YTDLSource.from_url(url, loop=self.bot.loop)
            ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)
            self._currentsong = player.title
            self._duration = player.duration
            await ctx.send('Now playing: {}'.format(player.title))

    @queue.group(invoke_without_command=True)
    async def list(self, ctx):
        """List the current queue"""
        if len(self.songqueue) >= 1:
            songs = []
            count = 0
            for x in self.songqueue:
                songs.append(f"{count}. {x['name']}")
            return await ctx.send(f'`{songs}`')
        else:
            return await ctx.send("No songs are currently in the queue")

    @list.command(hidden=True)
    async def raw(self, ctx):
        if len(self.songqueue) >= 1:
            return await ctx.send(f'`{self.songqueue}`')
        else:
            return await ctx.send("No songs are currently in the queue")

    @queue.command()
    async def remove(self, ctx, rm: int):
        """Remove a queued song"""
        if len(self.songqueue) >= 1 and not rm > len(self.songqueue) - 1:
            if self.songqueue[rm]['requester'].id == ctx.author.id or is_admin(ctx):
                await ctx.send(f"Removing {self.songqueue[rm]['name']} from queue")
                return self.songqueue.remove(self.songqueue[rm])
            if not self.songqueue[rm]['requester'].id == ctx.author.id:
                return await ctx.send(f"You didn't request this song! Ask {self.songqueue[rm]['requester'].name}")

    async def queuehandler(self):
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            if len(self.songqueue) >= 1:
                ctx = self.songqueue[0]['ctx']
                player = self.songqueue[0]['player']
                if not ctx.voice_client.is_playing():
                    ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)
                    self._currentsong = player.title
                    self._duration = player.duration
                    await ctx.send(f'Now playing: {player.title} requested by {self.songqueue[0]["requester"]}')
                    self.songqueue.pop(0)
            await asyncio.sleep(2)

    @commands.group(aliases=['skip'], invoke_without_command=True)
    async def next(self, ctx):
        if ctx.me.voice is None or not self._currentsong or not ctx.voice_client.is_playing():
            self.skips.clear()
            return await ctx.send("Nothing playing to skip...")
        if ctx.author not in self.skips and ctx.author in ctx.me.voice.channel.members:
            self.skips.append(ctx.author)
        elif ctx.author in self.skips:
            return await ctx.send(f"Nice try {ctx.author.display_name}, you already tried skipping")
        elif ctx.author not in ctx.me.voice.channel.members:
            return await ctx.\
                send(f"You aren't even listening {ctx.author.display_name}, why do you care what's playing?")
        if (len(self.skips) / (len(ctx.me.voice.channel.members)-1)) >= 0.65:
            if ctx.voice_client.is_playing():
                await ctx.send("Skipping")
                self.skips.clear()
                self._currentsong = ''
                self._duration = 0
                ctx.voice_client.stop()
        else:
            await ctx.send(f"{int((len(self.skips) / (len(ctx.me.voice.channel.members)-1))*100)}% "
                           f"voted to skip, need at least 65%")

    @next.command(aliases=['or', 'force', 'f'])
    @commands.check(is_admin)
    async def override(self, ctx):
        if ctx.me.voice is None:
            return None
        if ctx.voice_client.is_playing():
            await ctx.send(f"Force skipped by {str(ctx.author)}")
            self.skips.clear()
            self._currentsong = ''
            self._duration = 0
            ctx.voice_client.stop()

    @commands.command()
    async def volume(self, ctx, volume: float):
        """Changes the player's volume"""

        if ctx.voice_client is None:
            return await ctx.send("Not connected to a voice channel.")

        ctx.voice_client.source.volume = volume
        await ctx.send("Changed volume to {}%".format(volume))

    @commands.command(aliases=["disconnect"])
    async def stop(self, ctx):
        """Stops and disconnects the bot from voice"""
        self.songqueue.clear()
        self.skips.clear()
        self._currentsong = ''
        self._duration = 0
        await ctx.voice_client.disconnect()

    @commands.command()
    async def currentsong(self, ctx):
        if self._currentsong:
            dur = datetime.timedelta(seconds=self._duration)
            return await ctx.send(f'Currently playing: {self._currentsong} for a duration of {str(dur)}')
        else:
            return await ctx.send("Nothing currently playing.")


"""
@commands.command()
@commands.check(is_owner)
async def joinvc(self, ctx, channel: str = None):
    if ctx.me.voice is None:
        if channel is None:
            await ctx.author.voice.channel.connect()
        else:
            await discord.utils.get(ctx.message.guild.voice_channels, name=channel).connect()
    else:
        if channel is None:
            await ctx.me.move_to(ctx.author.voice.channel)
        else:
            await ctx.me.move_to(discord.utils.get(ctx.message.guild.voice_channels, name=channel))
"""


def setup(bot):
    bot.add_cog(Music(bot))
