import discord
import sys
from discord.ext import commands
from random import *
from cogs.utils.GlobalVars import *
import time


class PublicCmds:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def shelp(self, ctx):
        await ctx.send("```This is just a test\nwondering if this will work\nand if this is 3 lines```")

    @commands.command(aliases=["flip", "coin", "cointoss"])
    async def flipcoin(self, ctx):
        """Flips a coin."""
        if randint(0, 1) == 0:
            await ctx.send("Tails")
        else:
            await ctx.send("Heads")

    @commands.command()
    async def pick(self, ctx, *pick: str):
        """Randomly picks from a list of arguments given. Ex. pick 1 2 3."""
        await ctx.send(pick[randint(0, int(pick.__len__()-1))])

    @commands.command(aliases=["addrole"])
    async def getrole(self, ctx, *, addrole: str):
        """Gives you a game role."""
        alreadyhaveroles = []
        validrole = False
        toprole = 0
        for role in ctx.message.guild.roles:
            if role.name == "overwatch":
                toprole = role.position
        for role in ctx.message.guild.roles:
            if role.name == addrole and role.position <= toprole and role.position >= 1:
                validrole = True
        for role1 in ctx.message.author.roles:
            alreadyhaveroles.append(str(role1))
        if addrole in alreadyhaveroles:
            await ctx.message.add_reaction(emoji=xredemoji)
        else:
            if validrole:
                await ctx.message.author.add_roles(discord.utils.get(ctx.message.guild.roles, name=addrole))
                await ctx.message.add_reaction(emoji=checkmarkemoji)
            else:
                await ctx.message.add_reaction(emoji=xredemoji)

    @commands.command(aliases=["rmvrole"])
    async def removerole(self, ctx, *, rmvrole: str):
        """Removes a game role."""
        alreadyhaveroles = []
        validrole = False
        toprole = 0
        for role in ctx.message.guild.roles:
            if role.name == "overwatch":
                toprole = role.position
        for role in ctx.message.guild.roles:
            if role.name == rmvrole and role.position <= toprole and role.position >= 1:
                validrole = True
        for role1 in ctx.message.author.roles:
            alreadyhaveroles.append(str(role1))
        if rmvrole in alreadyhaveroles:
            if validrole:
                await ctx.message.author.remove_roles(discord.utils.get(ctx.message.guild.roles, name=rmvrole))
                await ctx.message.add_reaction(emoji=checkmarkemoji)
            else:
                await ctx.message.add_reaction(emoji=xredemoji)

    @commands.command()
    async def roll(self, ctx, maximumroll: int = 6):
        """Roles a standard 6 sided dice (or up to given number)."""
        await ctx.send(ctx.message.author.name + " rolled a " + str(randint(1, maximumroll)))

    @commands.command()
    async def membercount(self, ctx):
        """The amount of users connected to this server."""
        await ctx.send("This server has {} users connected.".format(ctx.message.guild.member_count))

    @commands.command()
    async def ping(self, ctx):
        """Calculates the ping time."""
        t1 = time.perf_counter()
        await ctx.trigger_typing()
        t2 = time.perf_counter()
        await ctx.send("Pong.\nTime: " + str(round((t2-t1)*1000)) + "ms")

    @commands.command()
    async def randomcolor(self, ctx):
        """Picks a random hex color and gives a preview."""
        randycolor = discord.Color(randint(0x000000, 0xFFFFFF))
        embed = discord.Embed(color=randycolor, description="Color: " + str(randycolor))
        await ctx.send(embed=embed)

    @commands.command(hidden=True)
    async def userinfo(self, ctx, mem: discord.Member = None):
        """Gives userinfo of yourself, or another user."""
        if mem is None:
            mem = ctx.message.author
        await ctx.trigger_typing()
        userrolelist = []
        for role in mem.roles:
            if role.name == '@everyone':
                userrolelist.append("everyone")
            else:
                userrolelist.append(role.name)
        embed = discord.Embed(title="Showing user info for: " + mem.display_name + "#" + str(mem.discriminator) + " : " + str(mem.id), description="User Status: {}\nPlaying: {}\nUser Avatar: {}\nUser Joined: {}\nUser Roles: {}".format(str(mem.status), str(mem.game), str(mem.avatar_url), str(mem.joined_at), str(userrolelist)), width=100)
        embed.set_image(url=mem.avatar_url.replace('size=1024', 'size=64'))
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(PublicCmds(bot))
