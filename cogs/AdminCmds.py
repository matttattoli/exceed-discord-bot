import random
import discord
from discord.ext import commands
import platform
import sys
from cogs.utils.checks import *
from cogs.utils.GlobalVars import *
from cogs.utils.debug import *


class AdminCmds:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True)
    async def checkmember(self, ctx):
        if is_admin(ctx):
            notverified = []
            for member in ctx.message.guild.members:
                is_verified = False
                for role in member.roles:
                    if role.name == "Member":
                        is_verified = True
                        break
                if not is_verified:
                    # await bot.add_roles(member, discord.utils.get(ctx.message.guild.roles,name="Member"))
                    notverified.append(str(member))
                    # debug_print("Added Member role to " + member.name)
            await ctx.send(str(notverified) + " do not have the Member role")

    @commands.command(hidden=True)
    async def purge(self, ctx, number: int):
        if is_admin(ctx):
            await ctx.message.channel.purge(limit=number + 1)
            await ctx.send('Deleted {} message(s)'.format(number), delete_after=2.5)

    @commands.command(aliases=["newrole"], hidden=True)
    async def createrole(self, ctx, *, rolename: str):
        if is_admin(ctx):
            currentroles = []
            for role in ctx.message.guild.roles:
                currentroles.append(role.name.lower())
            if rolename.lower() not in currentroles:
                await ctx.message.guild.create_role(name=rolename, mentionable=True, hoist=False, reason="New Game Role")
                await ctx.message.add_reaction(emoji=checkmarkemoji)
            else:
                await ctx.message.add_reaction(emoji=xredemoji)
        else:
            await ctx.message.add_reaction(emoji=xredemoji)

    @commands.command(hidden=True)
    async def deleterole(self, ctx, *, rolename: str):
        if is_admin(ctx):
            currentroles = []
            toprole = 0
            validrole = False
            for role in ctx.message.guild.roles:
                currentroles.append(role.name.lower())
                if role.name == 'overwatch':
                    toprole = role.position
            for role in ctx.message.guild.roles:
                if role.name == rolename and role.position <= toprole:
                    validrole = True
            if rolename.lower() in currentroles and validrole:
                await discord.utils.get(ctx.message.guild.roles, name=rolename).delete()
                await ctx.message.add_reaction(emoji=checkmarkemoji)
            else:
                await ctx.message.add_reaction(emoji=xredemoji)
        else:
            await ctx.message.add_reaction(emoji=xredemoji)


def setup(bot):
    bot.add_cog(AdminCmds(bot))
