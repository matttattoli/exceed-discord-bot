import discord
from discord.ext import commands
import platform
import sys
from cogs.utils.GlobalVars import *
from cogs.utils.checks import *
from testdict import *
debug = True


class TestCmds:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True)
    async def test22(self, ctx):
        if is_owner(ctx):
            pass
            await ctx.send(ctx.message.guild.me.status)

    @commands.command(hidden=True)
    async def test33(self, ctx):
        if is_owner(ctx):
            await ctx.send(str(self.bot.emojis))

    @commands.command(hidden=True)
    async def test44(self, ctx):
        if is_owner(ctx):
            await ctx.send(str(testlist))

    @commands.command(hidden=True)
    async def test55(self, ctx, appnd: str):
        if is_owner(ctx):
            testlist.append(appnd)
            f = open('testdict.py', 'w')
            f.write('testlist = ' + str(testlist))
            f.close()

    @commands.command(hidden=True)
    async def test12(self, ctx):
        if is_owner(ctx):
            f = open('testdict.py', 'w')
            f.write('testlist = ' + str(testlist))
            f.close()

    @commands.command(hidden=True)
    async def pings(self, ctx, mem: discord.Member, num: int=1):
        if is_owner(ctx):
            for i in range(num):
                await ctx.send(mem.mention)

    @commands.command(hidden=True)
    async def occupiedvchannels(self, ctx, status: bool):
        if is_owner(ctx):
            NewOccupiedChannelsEnabled = status
            await ctx.send(NewOccupiedChannelsEnabled)


def setup(bot):
    bot.add_cog(TestCmds(bot))

