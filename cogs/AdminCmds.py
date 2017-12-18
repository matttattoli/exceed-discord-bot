import random
import discord
from discord.ext import commands
import platform
import sys
from cogs.utils.checks import *
from cogs.utils.Emojis import *


class AdminCmds:
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
    async def setgame(self, ctx, *, setgameto: str):
        if is_owner(ctx):
            await self.bot.change_presence(game=discord.Game(name=setgameto))

    @commands.command(pass_context=True)
    async def setstatus(self, ctx, setstatusto: str):
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
    async def checkmember(self, ctx):
        if is_admin(ctx):
            notverified = []
            for member in ctx.message.server.members:
                is_verified = False
                for role in member.roles:
                    if role.name == "Member":
                        is_verified = True
                        break
                if not is_verified:
                    # await bot.add_roles(member, discord.utils.get(ctx.message.server.roles,name="Member"))
                    notverified.append(str(member))
                    # await bot.say("Added Member role to "+member.name)
            await self.bot.say(str(notverified) + " do not have the Member role")

    @commands.command(pass_context=True, hidden=True)
    async def purge(self, ctx, number: int):
        if is_admin(ctx):
            await self.bot.purge_from(ctx.message.channel, limit=number + 1)
            # await bot.send_message(ctx.message.channel, 'Deleted {} message(s)'.format(len(deleted)))

    @commands.command(pass_context=True, aliases=["newrole"], hidden=True)
    async def createrole(self, ctx, *, rolename: str):
        if is_admin(ctx):
            currentroles = []
            for role in ctx.message.server.roles:
                currentroles.append(role.name.lower())
            if rolename.lower() not in currentroles:
                await self.bot.create_role(ctx.message.server, name=rolename, mentionable=True, hoist=False, reason="New Game Role")
                await self.bot.add_reaction(ctx.message, emoji=checkmarkemoji)
            else:
                await self.bot.add_reaction(ctx.message, emoji=xredemoji)
        else:
            await self.bot.add_reaction(ctx.message, emoji=xredemoji)

    @commands.command(pass_context=True, hidden=True)
    async def deleterole(self, ctx, *, rolename: str):
        if is_admin(ctx):
            currentroles = []
            toprole = 0
            validrole = False
            for role in ctx.message.server.roles:
                currentroles.append(role.name.lower())
                if role.name == 'overwatch':
                    toprole = role.position
            for role in ctx.message.server.roles:
                if role.name == rolename and role.position <= toprole:
                    validrole = True
            if rolename.lower() in currentroles and validrole:
                await self.bot.delete_role(ctx.message.server, discord.utils.get(ctx.message.server.roles, name=rolename))
                await self.bot.add_reaction(ctx.message, emoji=checkmarkemoji)
            else:
                await self.bot.add_reaction(ctx.message, emoji=xredemoji)
        else:
            await self.bot.add_reaction(ctx.message, emoji=xredemoji)


def setup(bot):
    bot.add_cog(AdminCmds(bot))
