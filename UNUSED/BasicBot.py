import discord
import asyncio
from discord.ext.commands import Bot
from discord.ext import commands
import platform


client = Bot(description="Basic Bot by Habchy#1665", command_prefix="!!!", pm_help = True)

@client.event
async def on_ready():
	print('Logged in as '+client.user.name+' (ID:'+client.user.id+') | Connected to '+str(len(client.servers))+' servers | Connected to '+str(len(set(client.get_all_members())))+' users')
	print('--------')
	print('Current Discord.py Version: {} | Current Python Version: {}'.format(discord.__version__, platform.python_version()))
	print('--------')
	print('Use this link to invite {}:'.format(client.user.name))
	print('https://discordapp.com/oauth2/authorize?client_id={}&scope=bot&permissions=8'.format(client.user.id))



@client.command()
async def ping(*args):
	await client.say(":ping_pong: Pong!")
	
client.run('bot token')

# The help command is currently set to be Direct Messaged.
# If you would like to change that, change "pm_help = True" to "pm_help = False" on line 9.
