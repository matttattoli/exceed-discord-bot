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
description = "Pro bot to EXCEED your imagination"
bot = Bot(description=description, command_prefix=config["prefix"], pm_help=True)
startup_extensions = ["cogs.PublicCmds", "cogs.AdminCmds", "cogs.OwnerCmds", "cogs.TestCmds"]


@bot.event
async def on_ready():
    print('Logged in as ' + bot.user.name + ' (ID:' + str(bot.user.id) + ') | Connected to ' + str(len(bot.guilds)) + ' servers | Connected to ' + str(len(set(bot.get_all_members()))) + ' users')
    print('------')
    print('Use this link to invite {}:'.format(bot.user.name))
    print('https://discordapp.com/oauth2/authorize?client_id={}&scope=bot&permissions=8'.format(bot.user.id))
    print('Current Discord.py Version: {} | Current Python Version: {}'.format(discord.__version__, platform.python_version()))
    await bot.change_presence(game=discord.Game(name="What do you want?"), status=discord.Status.online)


@bot.command(hidden=True)
async def load(ctx, extension_name: str):
    if is_owner(ctx):
        try:
            bot.load_extension(extension_name)
        except (AttributeError, ImportError) as e:
            print("{}: {}".format(type(e).__name__, str(e)))
            return
        print("{} loaded.".format(extension_name))


@bot.command(name='reload', hidden=True)
async def _reload(ctx, module: str):
    if is_owner(ctx):
        """Reloads a module."""
        try:
            bot.unload_extension(module)
            bot.load_extension(module)
            debug_print(str(module))
        except Exception as e:
            await ctx.send(f'```py\n{traceback.format_exc()}\n```')
        else:
            await ctx.message.add_reaction('\N{OK HAND SIGN}')


@bot.command(name='reloadall', hidden=True)
async def _reloadall(ctx):
    if is_owner(ctx):
        """Reloads a module."""
    for module in bot.cogs:
        try:
            bot.unload_extension('cogs.' + module)
            bot.load_extension('cogs.' + module)
            debug_print('cogs.{}'.format(module))
        except Exception as e:
            await ctx.send(f'```py\n{traceback.format_exc()}\n```')
        else:
            await ctx.message.add_reaction('\N{OK HAND SIGN}')


@bot.command(hidden=True)
async def adminhelp(ctx):
    if is_admin(ctx):
        pass


@bot.command(hidden=True)
async def unload(ctx, extension_name: str):
    if is_owner(ctx):
            bot.unload_extension(extension_name)
            print("{} unloaded.".format(extension_name))


@bot.listen()
async def on_member_join(member):
    await bot.get_channel(382699994639237120).send(str(member) + " has joined the server.")
    await member.add_roles(discord.utils.get(member.guild.roles, name="Member"))


if __name__ == "__main__":
    for extension in startup_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {} \n {}'.format(extension, exc))
    bot.run(privateconfig["tokens"]["discord"], bot=True, reconnect=True)
