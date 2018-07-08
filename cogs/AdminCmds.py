import random
import discord
from discord.ext import commands
import platform
import sys
from cogs.utils.checks import *
from cogs.utils.GlobalVars import *
from cogs.utils.debug import *
from cogs.utils.Database import Database

class AdminCmds:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.check(is_admin)
    async def checkmember(self, ctx):
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

    @commands.group(invoke_without_command=True)
    @commands.check(is_admin)
    async def purge(self, ctx, number: int):
        await ctx.message.channel.purge(limit=number + 1)  # +1 to compensate for the users purge message.
        await ctx.send('Deleted {} message(s)'.format(number), delete_after=3)

    @purge.command()
    @commands.check(is_admin)
    async def user(self, ctx, mem: discord.Member, number: int):
        def is_user(m):
            return m.author == mem
        msgs = await ctx.message.channel.purge(limit=number, check=is_user)
        await ctx.send(f'Deleted {len(msgs)} message(s) from {str(mem)}', delete_after=3)

    # @commands.command()
    # @commands.check(is_admin)
    # async def deleterole(self, ctx, *, rolename: str):
    #     currentroles = []
    #     toprole = 0
    #     validrole = False
    #     for role in ctx.message.guild.roles:
    #         currentroles.append(role.name.lower())
    #         if role.name == 'overwatch':
    #             toprole = role.position
    #     for role in ctx.message.guild.roles:
    #         if role.name == rolename and role.position <= toprole:
    #             validrole = True
    #     if rolename.lower() in currentroles and validrole:
    #         await discord.utils.get(ctx.message.guild.roles, name=rolename).delete()
    #         await ctx.message.add_reaction(emoji=checkmarkemoji)
    #     else:
    #         await ctx.message.add_reaction(emoji=xredemoji)

    @commands.command()
    @commands.check(is_admin)
    async def setlogchannel(self, ctx, log_mode: int = 1):
        # setGuildLogChannel(ctx.guild.id, ctx.channel.id)
        # if getGuildLogChannel(ctx.guild.id) == ctx.channel.id:
        #     await ctx.message.add_reaction(emoji=checkmarkemoji)
        # else:
        #     await ctx.message.add_reaction(emoji=xredemoji)
        Database.setLogChannel(ctx.guild.id, log_mode, ctx.channel.id)

    @commands.command()
    @commands.check(is_admin)
    async def randomteams(self, ctx, chan1: discord.VoiceChannel, chan2: discord.VoiceChannel,
                          fromvc: discord.VoiceChannel=None):
        """Can be used to split a group of people into 2 random teams.
        \nSyntax: randomteams VChannel1 VChannel2 HomeChannel"""
        if fromvc is None:
            if ctx.author.voice is None:
                return None
            fromvc = ctx.author.voice.channel.id
        memberlist = ctx.guild.get_channel(fromvc).members
        movememto = []
        if len(memberlist) < 4:
            return None
        for x in range(len(memberlist)):
            if x >= int(len(memberlist)/2) and movememto.count(0) >= int(len(memberlist) / 2):
                movememto.append(1)
            elif x >= int(len(memberlist)/2) and movememto.count(1) >= int(len(memberlist) / 2):
                movememto.append(0)
            else:
                movememto.append(random.randint(0, 1))
        for x in range(len(memberlist)):
            if movememto[x] == 0:
                await memberlist[x].move_to(chan1)
            elif movememto[x] == 1:
                await memberlist[x].move_to(chan2)


def setup(bot):
    bot.add_cog(AdminCmds(bot))
