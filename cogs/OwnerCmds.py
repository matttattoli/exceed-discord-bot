import random
import discord
from discord.ext import commands
import platform
import sys
from cogs.utils.checks import *
from cogs.utils.Emojis import *


class OwnerCmds:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, hidden=True)
    async def roles(self, ctx):
        if is_owner(ctx):
            await self.bot.say(ctx.message.author.name + ":" + ctx.message.author.id)
            for role in ctx.message.server.roles:
                await self.bot.say(role.name + ":" + role.id)
            await self.bot.say("Idk why this takes me a while to find, but I'm done now")

    @commands.command(pass_context=True, hidden=True)
    async def setgame(self, ctx, *, setgameto: str = ''):
        if is_owner(ctx):
            await self.bot.change_presence(game=discord.Game(name=setgameto))

    @commands.command(pass_context=True, hidden=True)
    async def setstatus(self, ctx, setstatusto: str = 'on'):
        if is_owner(ctx):
            if setstatusto == 'online' or setstatusto == 'on':
                await self.bot.change_presence(status=discord.Status.online, game=discord.Game(name=str(ctx.message.server.me.game)))
            elif setstatusto == 'invisible' or setstatusto == 'inv' or setstatusto == 'invis':
                await self.bot.change_presence(status=discord.Status.invisible, game=discord.Game(name=str(ctx.message.server.me.game)))
            elif setstatusto == 'idle':
                await self.bot.change_presence(status=discord.Status.idle, game=discord.Game(name=str(ctx.message.server.me.game)))
            elif setstatusto == 'dnd' or setstatusto == 'donotdisturb' or setstatusto == 'do not disturb':
                await self.bot.change_presence(status=discord.Status.dnd, game=discord.Game(name=str(ctx.message.server.me.game)))

    @commands.command(pass_context=True, hidden=True)
    async def killbot(self, ctx):
        if is_owner(ctx):
            await self.bot.say("Bang bang :gun:")
            await self.bot.say("Bot Killed!")
            await self.bot.change_presence(game=discord.Game(name="KILLED!"))
            await self.bot.change_presence(status=discord.Status.invisible)
            await sys.exit()

    @commands.command(pass_context=True, hidden=True)
    async def say(self, ctx, channel: str, *, msg: str):
        if is_owner(ctx):
            if channel == '0':
                await self.bot.say(msg)
                await self.bot.delete_message(ctx.message)
            else:
                await self.bot.send_message(discord.utils.get(ctx.message.server.channels, name=channel), msg)

    @commands.command(pass_context=True, hidden=True)
    async def joinvc(self, ctx, channel: str = None):
        if is_owner(ctx):
            if channel is None:
                await self.bot.join_voice_channel(ctx.message.author.channel)
            else:
                await self.bot.join_voice_channel(discord.utils.get(ctx.message.server.channels, name=channel, type=discord.ChannelType.voice))

    @commands.command(pass_context=True, hidden=True)
    async def disconnect(self, ctx):
        if is_owner(ctx):
            await self.bot.disconnect()

    @commands.command(pass_context=True, hidden=True)
    async def tell(self, ctx, user: discord.Member, *, msg: str):
        if is_owner(ctx):
            await self.bot.send_message(user, msg)
            await self.bot.delete_message(ctx.message)


def setup(bot):
    bot.add_cog(OwnerCmds(bot))
