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


class TestCmds:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True)
    @commands.check(is_owner)
    async def test2(self, ctx):
        await ctx.send(str(self.bot.emojis))

    @commands.command()
    async def testcheckmc(self, ctx):
        async with aiohttp.ClientSession() as cs:
            with async_timeout.timeout(10):
                async with cs.get("https://api.mcsrvstat.us/1/gamfrk.noip.me:7777") as r:
                    data = await r.json()
        if "offline" in data:
            await ctx.send("Server offline")
        else:
            embed = discord.Embed(title="Showing server info for Minecraft")
            embed.add_field(name="IP", value="gamfrk.noip.me:7777", inline=False)
            if "list" in data["players"]:
                playersval = "{} - {}".format(data["players"]["online"], data["players"]["list"])
            else:
                playersval = data["players"]["online"]
            embed.add_field(name="Players", value=playersval, inline=False)
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(TestCmds(bot))

