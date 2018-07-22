import discord
from discord.ext import commands
import platform
import sys
from cogs.utils.GlobalVars import *
from cogs.utils.checks import *
from cogs.utils.debug import *
import asyncio
import aiohttp
import async_timeout
from cogs.utils.misc import printOverLimit


class TestCmds:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True)
    @commands.check(is_owner)
    async def test2(self, ctx):
        await ctx.send(str(self.bot.emojis))

    @commands.group()  # invoke_without_cmd
    @commands.check(is_owner)
    async def test(self, ctx):
        pass

    @test.command()
    @commands.check(is_admin)
    async def listemojis(self, ctx):
        allemojis = []
        for x in self.bot.emojis:
            if x.animated:
                allemojis.append(f'<a:{x.name}:{x.id}>')
            else:
                allemojis.append(f'<:{x.name}:{x.id}>')
        allemojis = ' '.join(allemojis)
        printout = printOverLimit(allemojis)
        if type(printout) == list:
            for x in printout:
                await ctx.send(x)
        else:
            await ctx.send(printout)

    @test.command()
    @commands.check(is_admin)
    async def listguildemojis(self, ctx):
        allemojis = []
        for x in ctx.guild.emojis:
            if x.animated:
                allemojis.append(f'<a:{x.name}:{x.id}>')
            else:
                allemojis.append(f'<:{x.name}:{x.id}>')
        allemojis = ' '.join(allemojis)
        printout = printOverLimit(allemojis)
        if type(printout) == list:
            for x in printout:
                await ctx.send(x)
        else:
            await ctx.send(printout)

    @test.command()
    @commands.check(is_owner)
    async def invitebot(self, ctx):
        await ctx.send(f"""You can use this link to try to invite the bot to another server, althought you may need\
        manage server roles. Also you might want to change the permissions argument in the link to 0, up to you.\
        https://discordapp.com/oauth2/authorize?client_id={self.bot.user.id}&scope=bot&permissions=8""")


def setup(bot):
    bot.add_cog(TestCmds(bot))

