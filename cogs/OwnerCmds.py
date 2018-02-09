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

class OwnerCmds:
    def __init__(self, bot):
        self.bot = bot
        self._last_result = None

    @commands.command(hidden=True)
    @commands.check(is_owner)
    async def exec(self, ctx, code: str):
        exec(code)

    @commands.command(hidden=True)
    @commands.check(is_owner)
    async def roles(self, ctx):
        listofroles = []
        for role in ctx.message.guild.roles:
            listofroles.append(role.name + ":" + str(role.id))
        embed = discord.Embed(title="List of Guild Roles", description=str(listofroles))
        await ctx.send(embed=embed)

    @commands.command(hidden=True)
    @commands.check(is_owner)
    async def setgame(self, ctx, *, setgameto: str = ''):
        await self.bot.change_presence(game=discord.Game(name=setgameto))

    @commands.command(hidden=True)
    @commands.check(is_owner)
    async def setstatus(self, ctx, setstatusto: str = 'on'):
        if setstatusto == 'online' or setstatusto == 'on':
            await self.bot.change_presence(status=discord.Status.online, game=discord.Game(name=str(ctx.me.game)))
        elif setstatusto == 'invisible' or setstatusto == 'inv' or setstatusto == 'invis':
            await self.bot.change_presence(status=discord.Status.invisible, game=discord.Game(name=str(ctx.me.game)))
        elif setstatusto == 'idle':
            await self.bot.change_presence(status=discord.Status.idle, game=discord.Game(name=str(ctx.me.game)))
        elif setstatusto == 'dnd' or setstatusto == 'donotdisturb' or setstatusto == 'do not disturb':
            await self.bot.change_presence(status=discord.Status.dnd, game=discord.Game(name=str(ctx.me.game)))

    @commands.command(hidden=True)
    @commands.check(is_owner)
    async def killbot(self, ctx):
        await ctx.send("Bang bang :gun:")
        await ctx.send("Bot Killed!")
        if ctx.me.voice is not None:
            await ctx.voice_client.disconnect()
        await self.bot.change_presence(game=discord.Game(name="KILLED!"))
        await self.bot.change_presence(status=discord.Status.invisible)
        await self.bot.logout()
        # await sys.exit()

    @commands.command(hidden=True)
    @commands.check(is_owner)
    async def say(self, ctx, channel: str, *, msg: str):
        if channel == '0':
            await ctx.send(msg)
            await ctx.message.delete()
        else:
            await discord.utils.get(ctx.message.guild.channels, name=channel).send(msg)
            await ctx.message.delete()

    @commands.command(hidden=True)
    @commands.check(is_owner)
    async def tell(self, ctx, user: discord.Member, *, msg: str):
        await user.send(msg)
        await ctx.message.delete()

    @commands.command(hidden=True)
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

    @commands.command(hidden=True)
    @commands.is_owner()
    async def disconnect(self, ctx):
        if ctx.me.voice is not None:
            await ctx.voice_client.disconnect()

    @commands.command(hidden=True)
    @commands.check(is_admin)
    async def mention(self, ctx, mem: discord.Member, num: int=1, msg: str=''):
        for i in range(num):
            await ctx.send(mem.mention + " " + msg)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def playa(self, ctx, src: str=None):
        await ctx.voice_client.play(src)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def stopa(self, ctx):
        await ctx.me.stop()

    # TODO: maybe something to move people around voice channels
    @commands.command(hidden=True)
    @commands.is_owner()
    async def fmove(self, ctx, user: discord.Member, room: discord.VoiceChannel, amount: int=1):
        for i in range(amount):
            await user.move_to(room)
            await asyncio.sleep(1)

    def cleanup_code(self, content):
        """Automatically removes code blocks from the code."""
        # remove ```py\n```
        if content.startswith('```') and content.endswith('```'):
            return '\n'.join(content.split('\n')[1:-1])
        # remove `foo`
        return content.strip('` \n')

    @commands.command(pass_context=True, hidden=True, name='eval')
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
