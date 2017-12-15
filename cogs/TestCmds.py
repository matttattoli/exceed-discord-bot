import discord
from discord.ext import commands
import platform
import sys
from cogs.utils.checks import *


class TestCmds:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def test22(self, ctx):
        if is_admin(ctx):
            pass
            await self.bot.say(ctx.message.server.me.status)

    @commands.command(pass_context=True)
    async def test33(self, ctx):
        if is_admin(ctx):
            lt = self.bot.get_all_emojis()
            for em in lt:
                await self.bot.say(em.name)

    @commands.command()
    async def test44(self, ctx):
        if is_admin(ctx):
            await self.bot.say(config["test"])

def setup(bot):
    bot.add_cog(TestCmds(bot))
