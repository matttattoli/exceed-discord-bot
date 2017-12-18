import discord
from discord.ext import commands
import platform
import sys
from cogs.utils.checks import *
from testdict import *
debug = True


class TestCmds:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, hidden=True)
    async def test22(self, ctx):
        if is_owner(ctx):
            pass
            await self.bot.say(ctx.message.server.me.status)

    @commands.command(pass_context=True, hidden=True)
    async def test33(self, ctx):
        if is_owner(ctx):
            lt = self.bot.get_all_emojis()
            for em in lt:
                await self.bot.say(em.name)

    @commands.command(pass_context=True, hidden=True)
    async def test44(self, ctx):
        if is_owner(ctx):
            await self.bot.say(str(testlist))

    @commands.command(pass_context=True, hidden=True)
    async def test55(self, ctx, appnd: str):
        if is_owner(ctx):
            testlist.append(appnd)
            f = open('testdict.py', 'w')
            f.write('testlist = ' + str(testlist))
            f.close()

    @commands.command(pass_context=True, hidden=True)
    async def test12(self, ctx):
        if is_owner(ctx):
            f = open('testdict.py', 'w')
            f.write('testlist = ' + str(testlist))
            f.close()

    @commands.command(pass_context=True, hidden=True)
    async def pings(self, ctx, mem: discord.Member, num: int=1):
        if is_owner(ctx):
            for i in range(num):
                await self.bot.say(mem.mention)





def setup(bot):
    bot.add_cog(TestCmds(bot))

