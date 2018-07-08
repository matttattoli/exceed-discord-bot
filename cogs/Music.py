import asyncio

import discord
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
        self.currentsong = ''
        self.audio_player = self.bot.loop.create_task(self.queuehandler())

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
        self.currentsong = player.title
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
            newsong = {"ctx": ctx, "url": url}
            self.songqueue.append(newsong)
            return await ctx.send(f"Added `{url}` to queue.")
        else:
            player = await YTDLSource.from_url(url, loop=self.bot.loop)
            ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)
            self.currentsong = player.title
            await ctx.send('Now playing: {}'.format(player.title))

    @queue.command()
    async def list(self, ctx):
        """List the current queue"""
        if len(self.songqueue) >= 1:
            return await ctx.send(f'`{self.songqueue}`')
        else:
            return await ctx.send("No songs are currently in the queue")

    async def queuehandler(self):
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            if len(self.songqueue) >= 1:
                ctx = self.songqueue[0]['ctx']
                url = self.songqueue[0]['url']
                if not ctx.voice_client.is_playing():
                    player = await YTDLSource.from_url(url, loop=self.bot.loop)
                    ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)
                    self.currentsong = player.title
                    await ctx.send('Now playing: {}'.format(player.title))
                    self.songqueue.pop(0)
            await asyncio.sleep(2)

    @commands.command(aliases=['skip'])
    async def next(self, ctx):
        if ctx.voice_client.is_playing():
            await ctx.send("Skipping")
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
        await ctx.voice_client.disconnect()


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
