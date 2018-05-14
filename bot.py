import discord
import asyncio
import aiohttp
from discord.ext.commands import Bot
from discord.ext import commands
from config import *
import platform
import sys
import json
from random import *
import traceback
from cogs.utils.checks import *
from cogs.utils.GlobalVars import *
from cogs.utils.debug import *
from cogs.utils.Database import Database
description = "Pro bot to EXCEED your imagination"
bot = Bot(description=description, command_prefix=commands.when_mentioned_or(config["prefix"]), pm_help=True)
startup_extensions = ("cogs.PublicCmds", "cogs.AdminCmds", "cogs.OwnerCmds", "cogs.TestCmds", "cogs.Music",
                      "cogs.Stats", "cogs.FunRoles")


@bot.event
async def on_ready():
    print('**********************************************************************')
    print('Logged in as ' + bot.user.name + ' (ID:' + str(bot.user.id) + ') | Connected to ' + str(len(bot.guilds)) +
          ' servers | Connected to ' + str(len(set(bot.get_all_members()))) + ' users')
    print('------')
    print('Use this link to invite {}:'.format(bot.user.name))
    print('https://discordapp.com/oauth2/authorize?client_id={}&scope=bot&permissions=8'.format(bot.user.id))
    print('Current Discord.py Version: {} | Current Python Version: {}'.format(discord.__version__,
                                                                               platform.python_version()))
    await bot.change_presence(game=discord.Game(name="What do you want?"), status=discord.Status.online)


@bot.command(hidden=True)
@commands.is_owner()
async def load(ctx, extension_name: str):
    try:
        bot.load_extension(extension_name)
        await ctx.message.add_reaction('\N{OK HAND SIGN}')
    except (AttributeError, ImportError) as e:
        print("{}: {}".format(type(e).__name__, str(e)))
        return
    print("{} loaded.".format(extension_name))


@bot.command(name='reload', hidden=True)
@commands.is_owner()
async def _reload(ctx, module: str):
    """Reloads a module."""
    try:
        bot.unload_extension(module)
        bot.load_extension(module)
        debug_print(str(module) + ' reloaded.')
    except Exception as e:
        await ctx.send(f'```py\n{traceback.format_exc()}\n```')
    else:
        await ctx.message.add_reaction('\N{OK HAND SIGN}')


@bot.command(name='reloadall', hidden=True)
@commands.is_owner()
async def _reloadall(ctx):
    """Reloads a module."""
    for module in bot.cogs:
        debug_print('cogs.{}'.format(module))
        try:
            bot.unload_extension('cogs.' + module)
            bot.load_extension('cogs.' + module)
        except Exception as e:
            await ctx.send(f'```py\n{traceback.format_exc()}\n```')
        else:
            await ctx.message.add_reaction('\N{OK HAND SIGN}')


@bot.command(hidden=True)
@commands.check(is_admin)
async def adminhelp(ctx):
    cmdlist = {}
    for cmd in bot.get_cog_commands('AdminCmds'):
        cmdlist[cmd.name] = cmd.aliases
    await ctx.author.send(cmdlist)


@bot.command(hidden=True)
@commands.check(is_owner)
async def ownerhelp(ctx):
    cmdlist = {}
    for cmd in bot.get_cog_commands('OwnerCmds'):
        cmdlist[cmd.name] = cmd.aliases
    for cmd in bot.get_cog_commands('TestCmds'):
        cmdlist[cmd.name] = cmd.aliases
    await ctx.author.send(cmdlist)


@bot.command(hidden=True)
@commands.is_owner()
async def unload(ctx, extension_name: str):
        bot.unload_extension(extension_name)
        await ctx.message.add_reaction('\N{OK HAND SIGN}')
        print("{} unloaded.".format(extension_name))


@bot.listen()
@commands.check(has_log_enabled)
async def on_member_join(member):
    await bot.get_channel(Database.getLogChannel(member.guild.id)).send(str(member) + " has joined the server.")
    await member.add_roles(discord.utils.get(member.guild.roles, name="Member"))


@bot.listen()
@commands.check(has_log_enabled)
async def on_member_remove(member):
    await bot.get_channel(Database.getLogChannel(member.guild.id)).send(str(member) + " has left the server.")


@bot.listen()
async def on_guild_join(guild):
    Database.initializeGuild(guild.id)


@bot.listen()
@commands.check(has_log_enabled)
async def on_guild_channel_create(channel):
    await bot.get_channel(Database.getLogChannel(channel.guild.id)).send(
        "{} {} has been created.".format(str(type(channel)).split('.')[2][:-2], channel.name))


@bot.listen()
@commands.check(has_log_enabled)
async def on_guild_channel_delete(channel):
    await bot.get_channel(Database.getLogChannel(channel.guild.id)).send(
        "{} {} has been deleted.".format(str(type(channel)).split('.')[2][:-2], channel.name))


@bot.listen()
@commands.check(has_log_enabled)
async def on_guild_role_create(role):
    await bot.get_channel(Database.getLogChannel(role.guild.id)).send("Role {} has been created.".format(role.name))


@bot.listen()
@commands.check(has_log_enabled)
async def on_guild_role_delete(role):
    await bot.get_channel(Database.getLogChannel(role.guild.id)).send("Role {} has been deleted.".format(role.name))


@bot.listen()
@commands.check(has_log_enabled)
async def on_member_update(before, after):
    descr = ''
    if not before.display_name == after.display_name:
        descr = "Name changed from {} to {}".format(before.display_name, after.display_name)
    if not str(before.roles) == str(after.roles):
        changedrole = str(set(before.roles) ^ set(after.roles))
        changedrole = changedrole.split('\'')[1]
        if changedrole in str(before.roles):
            changedrole = changedrole + ' has been removed.'
        else:
            changedrole = changedrole + ' has been added.'
        if not descr == '':
            descr = descr + "\n Role {}".format(changedrole)
        else:
            descr = "Role " + changedrole
    if not descr == '':
        embed = discord.Embed(title="User {} : {} has been updated.".format(str(before), before.id), description=descr)
        await bot.get_channel(Database.getLogChannel(before.guild.id)).send(embed=embed)


@bot.listen()
@commands.check(has_log_enabled)
async def on_member_ban(guild, user):
    await bot.get_channel(Database.getLogChannel(guild.id)).send('User {} : {} has been banned.'
                                                                 .format(str(user), user.id))


@bot.listen()
@commands.check(has_log_enabled)
async def on_member_unban(guild, user):
    await bot.get_channel(Database.getLogChannel(guild.id)).send('User {} : {} has been unbanned.'
                                                                 .format(str(user), user.id))

if __name__ == "__main__":
    for extension in startup_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {} \n {}'.format(extension, exc))
    bot.run(privateconfig["tokens"]["discord"], bot=True, reconnect=True)
