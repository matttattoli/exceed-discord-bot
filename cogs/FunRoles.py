import discord
from discord.ext import commands
from cogs.utils.checks import *
from cogs.utils.GlobalVars import *
from cogs.utils.debug import *
from cogs.utils.Database import Database


class FunRoles:
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True, aliases=["roles", "funroles"])
    async def role(self, ctx):
        pass

    @role.command()
    async def list(self, ctx):
        return await ctx.send(Database.getFunRoles(ctx.guild.id))

    @role.command()
    @commands.check(is_admin)
    async def create(self, ctx, *, rolename: str):
        roleobj = discord.utils.get(ctx.guild.roles, name=rolename)
        Database.addfunrole(ctx.guild.id, roleobj)
        if Database.isfunrole(ctx.guild.id, roleobj.id):
            return await ctx.message.add_reaction(emoji=checkmarkemoji)
        else:
            return await ctx.message.add_reaction(emoji=redxemoji)

    @role.command()
    @commands.check(is_admin)
    async def masscreate(self, ctx, *rolename: discord.Role):
        rolesadded = []
        rolesnotadded = []
        for role in rolename:
            Database.addfunrole(ctx.guild.id, role)
            if Database.isfunrole(ctx.guild.id, role.id):
                rolesadded.append(role.name)
            else:
                rolesnotadded.append(role.name)
        await ctx.message.add_reaction(emoji=checkmarkemoji)
        return await ctx.send(f"Roles successfully added: {rolesadded} \n Unsuccesss: {rolesnotadded}")

    @role.command()
    @commands.check(is_admin)
    async def delete(self, ctx, *, rolename: str):
        roleobj = discord.utils.get(ctx.guild.roles, name=rolename)
        if Database.isfunrole(ctx.guild.id, roleobj.id):
            Database.removefunrole(ctx.guild.id, roleobj)
            if Database.isfunrole(ctx.guild.id, roleobj.id):
                return await ctx.message.add_reaction(emoji=redxemoji)
            else:
                return await ctx.message.add_reaction(emoji=checkmarkemoji)
        else:
            return await ctx.message.add_reaction(emoji=redxemoji)

    @role.command()
    @commands.check(is_admin)
    async def massdelete(self, ctx, *rolename: discord.Role):
        rolesremoved = []
        rolesnotremoved = []
        for role in rolename:
            Database.removefunrole(ctx.guild.id, role)
            if Database.isfunrole(ctx.guild.id, role.id):
                rolesnotremoved.append(role.name)
            else:
                rolesremoved.append(role.name)
        await ctx.message.add_reaction(emoji=checkmarkemoji)
        return await ctx.send(f"Roles successfully removed: {rolesremoved} \n Unsuccesss: {rolesnotremoved}")

    @role.command(aliases=['add'])
    async def join(self, ctx, *, rolename: str):
        roleobj = discord.utils.get(ctx.message.guild.roles, name=rolename)
        if roleobj is None:
            await ctx.send("Oops that role doesn't exist.")  # debug purposes
            return await ctx.message.add_reaction(emoji=redxemoji)
        if roleobj in ctx.author.roles:
            await ctx.send("Oops you already have that role.")  # debug purposes
            return await ctx.message.add_reaction(emoji=redxemoji)
        if Database.isfunrole(ctx.guild.id, roleobj.id):
            await ctx.message.author.add_roles(roleobj)
            return await ctx.message.add_reaction(emoji=checkmarkemoji)
        else:
            return await ctx.message.add_reaction(emoji=redxemoji)

    @role.command(aliases=['remove'])
    async def leave(self, ctx, *, rolename: str):
        roleobj = discord.utils.get(ctx.message.guild.roles, name=rolename)
        if roleobj is None:
            await ctx.send("Oops that role doesn't exist.")  # debug purposes
            return await ctx.message.add_reaction(emoji=redxemoji)
        if roleobj in ctx.author.roles and Database.isfunrole(ctx.guild.id, roleobj.id):
            await ctx.message.author.remove_roles(roleobj)
            return await ctx.message.add_reaction(emoji=checkmarkemoji)
        else:
            return await ctx.message.add_reaction(emoji=redxemoji)


def setup(bot):
    bot.add_cog(FunRoles(bot))
