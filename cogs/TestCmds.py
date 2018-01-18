import discord
from discord.ext import commands
import platform
import sys
from cogs.utils.GlobalVars import *
from cogs.utils.checks import *
from testdict import *
from cogs.utils.debug import *
import asyncio


class TestCmds:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True)
    @commands.check(is_owner)
    async def test1(self, ctx):
        await ctx.send(ctx.message.guild.me.status + " : " + ctx.message.guild.me.game)

    @commands.command(hidden=True)
    @commands.check(is_owner)
    async def test2(self, ctx):
        await ctx.send(str(self.bot.emojis))

    @commands.command(hidden=True)
    @commands.check(is_owner)
    async def test3(self, ctx):
        await ctx.send(str(testlist))

    @commands.command(hidden=True)
    @commands.check(is_owner)
    async def test4(self, ctx, appnd: str):
        testlist.append(appnd)
        f = open('testdict.py', 'w')
        f.write('testlist = ' + str(testlist))
        f.close()

    @commands.command(hidden=True)
    @commands.check(is_owner)
    async def test5(self, ctx):
        f = open('testdict.py', 'w')
        f.write('testlist = ' + str(testlist))
        f.close()


"""
    @commands.command(hidden=True)
    @commands.check(is_admin)
    async def wank(self, ctx, ww: str):
        times = 1
        if ww == 'slow':
            times = 0.3
        elif ww == 'fast':
            times = 0.1
        msg = await ctx.send('8=mm===D')
        for i in range(100):
            await msg.edit(content='8=mm===D')
            await asyncio.sleep(times)
            await msg.edit(content='8==mm==D')
            await asyncio.sleep(times)
            await msg.edit(content='8===mm=D')
            await asyncio.sleep(times)
            await msg.edit(content='8==mm==D')
            await asyncio.sleep(times)
"""


"""
    @commands.command(hidden=True)
    @commands.check(is_owner)
    async def test6(self, ctx):
        data = {"1st": ["this is a test", '1', 2, 4], '2nd': 'idk what im doin'}
        json.dump(data, open('test6.json', 'w'), indent=4, sort_keys=True)
        data2 = {"name": 'alpha', 'num': [1, 2, 3, 4, 5, 6]}
        data3 = [1, 2, 3, 4, 5, 6]
        json.dump(data2, indent=4, sort_keys=True, fp=open('test6.json', 'w'))
        # json.dump(data3, open('test6.json', 'w+'), indent=4, sort_keys=True)



    @commands.command(hidden=True)
    @commands.check(is_owner)
    async def occupiedvchannels(self, ctx, status: bool):
        NewOccupiedChannelsEnabled = status
        await ctx.send(NewOccupiedChannelsEnabled)
"""


def setup(bot):
    bot.add_cog(TestCmds(bot))

