import random
import traceback
import discord
from discord.ext import commands
import platform
import sys
from cogs.utils.checks import *
from cogs.utils.GlobalVars import *
from cogs.utils.debug import *
import asyncio
from contextlib import redirect_stdout
import io
import inspect
import textwrap
import datetime
from collections import Counter
from cogs.utils.Database import Database

class OwnerCmds:
    def __init__(self, bot):
        self.bot = bot
        self._last_result = None

    @commands.command()
    @commands.check(is_owner)
    async def printroles(self, ctx):
        listofroles = []
        for role in ctx.message.guild.roles:
            listofroles.append(role.name + ":" + str(role.id))
        embed = discord.Embed(title="List of Guild Roles", description=str(listofroles))
        await ctx.send(embed=embed)

    @commands.group()
    @commands.check(is_owner)
    async def presence(self, ctx):
        pass

    @presence.command(aliases=['gaming', 'play', 'playing'])
    @commands.check(is_owner)
    async def game(self, ctx, *, setgameto: str = ''):
        await self.bot.change_presence(activity=discord.Game(name=setgameto), status=ctx.me.status)

    @presence.command(aliases=['streaming'])
    @commands.check(is_owner)
    async def stream(self, ctx, streamname: str, streamurl: str = ''):
        if not streamurl[:8] == "https://":
            return False
        await self.bot.change_presence(activity=discord.Streaming(name=streamname, url=streamurl), status=ctx.me.status)

    @presence.command(aliases=['watching'])
    @commands.check(is_owner)
    async def watch(self, ctx, *, setgameto: str = ''):
        await self.bot.change_presence(activity=discord.Activity(name=setgameto, type=discord.ActivityType.watching),
                                       status=ctx.me.status)

    @presence.command(aliases=['listening'])
    @commands.check(is_owner)
    async def listen(self, ctx, *, setgameto: str = ''):
        await self.bot.change_presence(
            activity=discord.Activity(name=setgameto, type=discord.ActivityType.listening),
            status=ctx.me.status)

    @presence.command()
    @commands.check(is_owner)
    async def status(self, ctx, setstatusto: str = 'on'):
        if setstatusto == 'online' or setstatusto == 'on':
            await self.bot.change_presence(status=discord.Status.online, activity=discord.Activity(
                name=ctx.me.activity.name, type=ctx.me.activity.type))
        elif setstatusto == 'invisible' or setstatusto == 'inv' or setstatusto == 'invis':
            await self.bot.change_presence(status=discord.Status.invisible, activity=discord.Activity(
                name=ctx.me.activity.name, type=ctx.me.activity.type))
        elif setstatusto == 'idle':
            await self.bot.change_presence(status=discord.Status.idle, activity=discord.Activity(
                name=ctx.me.activity.name, type=ctx.me.activity.type))
        elif setstatusto == 'dnd' or setstatusto == 'donotdisturb' or setstatusto == 'do not disturb':
            await self.bot.change_presence(status=discord.Status.dnd, activity=discord.Activity(
                name=ctx.me.activity.name, type=ctx.me.activity.type))

    @commands.command()
    @commands.check(is_owner)
    async def killbot(self, ctx):
        await ctx.send("Bang bang :gun:")
        await ctx.send("Bot Killed!")
        if ctx.me.voice is not None:
            await ctx.voice_client.disconnect()
            await self.bot.change_presence(status=discord.Status.dnd, activity=discord.Game("KILLED"))
        await self.bot.change_presence(status=discord.Status.invisible)
        await self.bot.logout()
        # await sys.exit()

    @commands.command()
    @commands.check(is_owner)
    async def say(self, ctx, channel: str, *, msg: str):
        if channel == '0':
            await ctx.send(msg)
            await ctx.message.delete()
        elif channel.isnumeric():
            channel = self.bot.get_channel(int(channel))
            await channel.send(msg)
            await ctx.message.delete()
        else:
            await discord.utils.get(ctx.message.guild.channels, name=channel).send(msg)
            await ctx.message.delete()

    @commands.command()
    @commands.check(is_owner)
    async def tell(self, ctx, user: discord.Member, *, msg: str):
        await user.send(msg)
        await ctx.message.delete()

    @commands.command()
    @commands.check(is_admin)
        for _ in range(num):
            await ctx.send(mem.mention + " " + msg)

    @commands.command()
    @commands.is_owner()
    async def fmove(self, ctx, user: discord.Member, room: discord.VoiceChannel, amount: int=1):
        for _ in range(amount):
            await user.move_to(room)
            await asyncio.sleep(1)

    @commands.group()
    @commands.check(is_owner)
    async def blacklist(self, ctx):
        pass

    @blacklist.command()
    @commands.check(is_owner)
    async def add(self, ctx, user: discord.Member):
        Database.blacklistUser(user.id, user.display_name, datetime.datetime.now())
        await ctx.send(f"{str(user)} got blacklisted from using EXCEED-BOT")

    @blacklist.command()
    @commands.check(is_owner)
    async def remove(self, ctx, user: discord.Member):
        if user.id not in Database.getblacklist():
            Database.unblacklistUser(user.id)
            await ctx.send(f"{str(user)} got unnblacklisted from using EXCEED-BOT")

    @blacklist.command(aliases=['list'])
    @commands.check(is_owner)
    async def _list(self, ctx):
        return await ctx.send(Database.getblacklist())

    def cleanup_code(self, content):
        """Automatically removes code blocks from the code."""
        # remove ```py\n```
        if content.startswith('```') and content.endswith('```'):
            return '\n'.join(content.split('\n')[1:-1])
        # remove `foo`
        return content.strip('` \n')

    @commands.command(name='eval')
    @commands.is_owner()
    async def _eval(self, ctx, *, body: str):
        """Evaluates a code"""

        env = {
            'bot': self.bot,
            'ctx': ctx,
            'channel': ctx.channel,
            'author': ctx.author,
            'guild': ctx.guild,
            'message': ctx.message,
            '_': self._last_result
        }

        env.update(globals())

        body = self.cleanup_code(body)
        stdout = io.StringIO()

        to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'

        try:
            exec(to_compile, env)
        except Exception as e:
            return await ctx.send(f'```py\n{e.__class__.__name__}: {e}\n```')

        func = env['func']
        try:
            with redirect_stdout(stdout):
                ret = await func()
        except Exception as e:
            value = stdout.getvalue()
            await ctx.send(f'```py\n{value}{traceback.format_exc()}\n```')
        else:
            value = stdout.getvalue()
            try:
                await ctx.message.add_reaction('\u2705')
            except:
                pass

            if ret is None:
                if value:
                    await ctx.send(f'```py\n{value}\n```')
            else:
                self._last_result = ret
                await ctx.send(f'```py\n{value}{ret}\n```')


def setup(bot):
    bot.add_cog(OwnerCmds(bot))
