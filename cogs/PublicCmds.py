import discord
import sys
from discord.ext import commands
from random import *

xredemoji = '\N{CROSS MARK}'
checkmarkemoji = '\N{WHITE HEAVY CHECK MARK}'


class PublicCmds:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["flip", "coin"])
    async def flipcoin(self):
        if randint(0, 1) == 0:
            await self.bot.say("Tails")
        else:
            await self.bot.say("Heads")

    @commands.command()
    async def pick(self, *pick: str):
        await self.bot.say(pick[randint(0, int(pick.__len__()-1))])

    @commands.command(pass_context=True, aliases=["addrole"])
    async def getrole(self, ctx, *, addrole: str):
        alreadyhaveroles = []
        validrole = False
        toprole = 0
        for role in ctx.message.server.roles:
            if role.name == "overwatch":
                toprole = role.position
        for role in ctx.message.server.roles:
            if role.name == addrole and role.position <= toprole and role.position >= 1:
                validrole = True
        for role1 in ctx.message.author.roles:
            alreadyhaveroles.append(str(role1))
        if addrole in alreadyhaveroles:
            await self.bot.add_reaction(ctx.message, emoji=xredemoji)
            pass
        else:
            if validrole:
                await self.bot.add_roles(ctx.message.author, discord.utils.get(ctx.message.server.roles, name=addrole))
                await self.bot.add_reaction(ctx.message, emoji=checkmarkemoji)
            else:
                await self.bot.add_reaction(ctx.message, emoji=xredemoji)

    @commands.command(pass_context=True, aliases=["rmvrole"])
    async def removerole(self, ctx, *, rmvrole: str):
        alreadyhaveroles = []
        validrole = False
        toprole = 0
        for role in ctx.message.server.roles:
            if role.name == "overwatch":
                toprole = role.position
        for role in ctx.message.server.roles:
            if role.name == rmvrole and role.position <= toprole and role.position >= 1:
                validrole = True
        for role1 in ctx.message.author.roles:
            alreadyhaveroles.append(str(role1))
        if rmvrole in alreadyhaveroles:
            if validrole:
                await self.bot.remove_roles(ctx.message.author, discord.utils.get(ctx.message.server.roles, name=rmvrole))
                await self.bot.add_reaction(ctx.message, emoji=checkmarkemoji)
        else:
            pass
            await self.bot.add_reaction(ctx.message, emoji=xredemoji)

    @commands.command(pass_context=True)
    async def roll(self, ctx, maximumroll: int = 6):
        await self.bot.say(ctx.message.author.name + " rolled a " + str(randint(1, maximumroll)))

    @commands.command(pass_context=True)
    async def membercount(self, ctx):
        await self.bot.say("This server has {} users connected.".format(ctx.message.server.member_count))

    @commands.command()
    async def ping(self):
        await self.bot.say(":ping_pong: Pong!")

    @commands.command()
    async def randomcolor(self):
        randycolor = discord.Color(randint(0x000000, 0xFFFFFF))
        embed = discord.Embed(color=randycolor, description="Color: " + str(randycolor))
        # await self.bot.say("Color: " + str(randycolor))
        await self.bot.say(embed=embed)


def setup(bot):
    bot.add_cog(PublicCmds(bot))
