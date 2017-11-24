import discord
import asyncio
import aiohttp
from discord.ext.commands import Bot
from discord.ext import commands
from config import config
import platform
import sys
import json


client = Bot(description=config["description"], command_prefix=config["prefix"], pm_help = True)

@client.event
async def on_ready():
    print('Logged in as '+client.user.name+' (ID:'+client.user.id+') | Connected to '+str(len(client.servers))+' servers | Connected to '+str(len(set(client.get_all_members())))+' users')
    print('------')
    print('Use this link to invite {}:'.format(client.user.name))
    print('https://discordapp.com/oauth2/authorize?client_id={}&scope=bot&permissions=8'.format(client.user.id))
    print('Current Discord.py Version: {} | Current Python Version: {}'.format(discord.__version__, platform.python_version()))
    await client.change_presence(game=discord.Game(name="What do you want?"))

@client.event
async def on_message(message):
    if message.content.startswith(config["prefix"]+'test'):
        counter = 0
        tmp = await client.send_message(message.channel, 'Calculating messages...')
        async for log in client.logs_from(message.channel, limit=100):
            if log.author == message.author:
                counter += 1
        await client.edit_message(tmp, 'You have {} messages.'.format(counter))
    elif message.content.startswith(config["prefix"]+'sleep'):
        await asyncio.sleep(5)
        await client.send_message(message.channel, 'Done sleeping')
    elif message.content.startswith(config["prefix"]+'terminateall'):
        await client.send_message(message.channel, 'Terminating all clients, including you @'+str(message.author)+' !')
        await asyncio.sleep(5)
        await client.send_message(message.channel, 'Termination complete.')
    elif message.content.startswith(config["prefix"]+'killbot'):
        await client.send_message(message.channel, 'Bot killed!')
        await client.change_presence(game=discord.Game(name="Offline"))
        sys.exit()
    elif message.content.startswith(config["prefix"]+'ping'):
        await client.send_message(message.channel, ":ping_pong: Pong!")
    elif message.content.startswith(config["prefix"]+'getrole'):
        role = message.content[len(config["prefix"]+'getrole'):].strip().lower()
        #await client.
        await client.send_message(message.channel, discord.utils.get(message.server.roles, name=role))
        #await client.add_roles(message.author, role)
        await client.send_message(message.channel, discord.Role)

@client.command(pass_context=True)
async def testcmd(self, ctx, user: discord.Member):
    author = ctx.message.author
    print(author.id) # This is your author id number
    print(user.id) # This is the user's id
    print(author.name) # This is the author's id
    print(user.name) # This is the user's name



client.run(config["tokens"]["discord"],bot=True,reconnect=True)
