import discord
import sys
from discord.ext import commands
from random import *

xredemoji = '\N{CROSS MARK}'
checkmarkemoji = '\N{WHITE HEAVY CHECK MARK}'


class PublicCmds:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["flip", "coin", "cointoss"])
    async def flipcoin(self):
        """Flips a coin."""
        if randint(0, 1) == 0:
            await self.bot.say("Tails")
        else:
            await self.bot.say("Heads")

    @commands.command()
    async def pick(self, *pick: str):
        """Randomly picks from a list of arguments given. Ex. pick 1 2 3."""
        await self.bot.say(pick[randint(0, int(pick.__len__()-1))])

    @commands.command(pass_context=True, aliases=["addrole"])
    async def getrole(self, ctx, *, addrole: str):
        """Gives you a game role."""
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
        """Removes a game role."""
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
        """Roles a standard 6 sided dice (or up to given number)."""
        await self.bot.say(ctx.message.author.name + " rolled a " + str(randint(1, maximumroll)))

    @commands.command(pass_context=True)
    async def membercount(self, ctx):
        """The amount of users connected to this server."""
        await self.bot.say("This server has {} users connected.".format(ctx.message.server.member_count))

    @commands.command()
    async def ping(self):
        await self.bot.say(":ping_pong: Pong!")

    @commands.command()
    async def randomcolor(self):
        """Picks a random hex color and gives a preview."""
        randycolor = discord.Color(randint(0x000000, 0xFFFFFF))
        embed = discord.Embed(color=randycolor, description="Color: " + str(randycolor))
        # await self.bot.say("Color: " + str(randycolor))
        await self.bot.say(embed=embed)

    @commands.command(pass_context=True, hidden=True)
    async def userinfo(self, ctx, mem: discord.Member = None):
        """Gives userinfo of yourself, or another user."""
        if mem is None:
            mem = ctx.message.author
        await self.bot.send_typing(ctx.message.channel)
        userrolelist = []
        for role in mem.roles:
            if role.name == '@everyone':
                userrolelist.append("everyone")
            else:
                userrolelist.append(role.name)
        embed = discord.Embed(title="Showing user info for: " + mem.display_name + "#" + mem.discriminator + " : " + mem.id, description="User Status: {}\nPlaying: {}\nUser Avatar: {}\nUser Joined: {}\nUser Roles: {}".format(mem.status, mem.game, mem.avatar_url, mem.joined_at, str(userrolelist)), width=100)
        embed.set_image(url=mem.avatar_url.replace('size=1024', 'size=64'))
        await self.bot.say(embed=embed)


def setup(bot):
    bot.add_cog(PublicCmds(bot))
