import discord
import asyncio
import aiohttp
from discord.ext.commands import Bot
from discord.ext import commands
from config import config
import platform
import sys
import json
from random import *
from cogs.utils.checks import *

"""class Bot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)"""

bot = Bot(description=config["description"], command_prefix=config["prefix"], pm_help=True)
xredemoji = '\N{CROSS MARK}'
checkmarkemoji = '\N{WHITE HEAVY CHECK MARK}'

@bot.event
async def on_ready():
    print('Logged in as ' + bot.user.name + ' (ID:' + bot.user.id + ') | Connected to ' + str(
        len(bot.servers)) + ' servers | Connected to ' + str(len(set(bot.get_all_members()))) + ' users')
    print('------')
    print('Use this link to invite {}:'.format(bot.user.name))
    print('https://discordapp.com/oauth2/authorize?client_id={}&scope=bot&permissions=8'.format(bot.user.id))
    print('Current Discord.py Version: {} | Current Python Version: {}'.format(discord.__version__, platform.python_version()))
    await bot.change_presence(status=discord.Status.online)
    await bot.change_presence(game=discord.Game(name="What do you want?"))


@bot.command(pass_context=True)
async def roles(ctx):
    if is_admin(ctx):
        await bot.say(ctx.message.author.name + ":" + ctx.message.author.id)
        for role in ctx.message.server.roles:
            await bot.say(role.name + ":" + role.id)
        await bot.say("Idk why this takes me a while to find, but I'm done now")


@bot.command()
async def hey():
    await bot.say("hey baby gurr")


@bot.command(pass_context=True)
async def setgame(ctx, *, setgameto: str):
    if is_admin(ctx):
        # setgameto = ctx.message.content[len(str(config["prefix"])) + 7:]
        await bot.change_presence(game=discord.Game(name=setgameto))


@bot.command(pass_context=True)
async def setstatus(ctx, setstatusto: str):
    if is_admin(ctx):
        if setstatusto == 'online' or setstatusto == 'on':
            await bot.change_presence(status=discord.Status.online)
        elif setstatusto == 'invisible' or setstatusto == 'inv' or setstatusto == 'invis':
            await bot.change_presence(status=discord.Status.invisible)
        elif setstatusto == 'idle':
            await bot.change_presence(status=discord.Status.idle)
        elif setstatusto == 'dnd' or setstatusto == 'donotdisturb' or setstatusto == 'do not disturb':
            await bot.change_presence(status=discord.Status.dnd)


@bot.command(pass_context=True)
async def killbot(ctx):
    if is_admin(ctx):
        await bot.say("Bang bang :gun:")
        await bot.say("Bot Killed!")
        await bot.change_presence(game=discord.Game(name="KILLED!"))
        await bot.change_presence(status=discord.Status.invisible)
        await sys.exit()


@bot.command(aliases=["flip", "coin"])
async def flipcoin():
    if randint(0, 1) == 0:
        await bot.say("Tails")
    else:
        await bot.say("Heads")


"""
@bot.command(pass_context=True)
async def getrole(ctx):
    role = ctx.message.content[len(str(config["prefix"]))+8:]
    #await bot.say(role)
    if role in config["getroles"]:
        #await bot.say("is in getroles dict")
        roleid = config["roles"][role]
        #await bot.say(role+":"+str(roleid))
        roles = []
        for role1 in ctx.message.author.roles:
            roles.append(str(role1))
        if role in roles:
            pass
            #await bot.say(str(role)+" is already in your roles!")
            #await bot.add_reaction(ctx.message, discord.utils.get(bot.get_all_emojis(), name="x"))
        if not role in roles:
            #await bot.say("Attempting to give role: " + config["roles"][role])
            await bot.add_roles(ctx.message.author, discord.utils.get(ctx.message.server.roles,name=role))
            #emoji = discord.utils.get(bot.get_all_emojis(), name='white_check_mark')
            
            await bot.add_reaction(ctx.message, emoji)
            #await bot.say(role + " role given to " + ctx.message.author.mention)

@bot.command(pass_context=True)
async def removerole(ctx):
    role = str(ctx.message.content[len(str(config["prefix"]))+11:])
    #await bot.say(role)
    if role in config["getroles"]:
        #await bot.say("\""+role+"\"is in getroles dict")
        roleid = config["roles"][role]
        #await bot.say(role+":"+str(roleid))
        roles = []
        for role1 in ctx.message.author.roles:
            roles.append(str(role1))
        if not role in roles:
            pass
            #await bot.say(str(role)+" is not in your roles!")
            #await bot.add_reaction(ctx.message, discord.utils.get(bot.get_all_emojis(), name="x"))
        if role in roles:
            #await bot.say("Attempting to remove role: " + config["roles"][role])
            await bot.remove_roles(ctx.message.author, discord.utils.get(ctx.message.server.roles,name=role))
            #await bot.add_reaction(ctx.message,":white_check_mark:")
            #await bot.say(role + " role removed from " + ctx.message.author.mention)
"""


@bot.command(pass_context=True, aliases=["addrole"])
async def getrole(ctx, *, addrole: str):
    # role = ctx.message.content[len(str(config["prefix"]))+8:]
    alreadyhaveroles = []
    validrole = False
    toprole = 0
    # rolee = discord.utils.get(member.server.roles,name=addrole)
    for role in ctx.message.server.roles:
        if role.name == "overwatch":
            toprole = role.position
    for role in ctx.message.server.roles:
        if role.name == addrole and role.position <= toprole and role.position >= 1:
            validrole = True
    for role1 in ctx.message.author.roles:
        alreadyhaveroles.append(str(role1))
    if addrole in alreadyhaveroles:
        await bot.add_reaction(ctx.message, emoji='\N{CROSS MARK}')
        pass
    else:
        if validrole:
            await bot.add_roles(ctx.message.author, discord.utils.get(ctx.message.server.roles, name=addrole))
            await bot.add_reaction(ctx.message, emoji='\N{WHITE HEAVY CHECK MARK}')
        else:
            await bot.add_reaction(ctx.message, emoji='\N{CROSS MARK}')


@bot.command(pass_context=True, aliases=["rmvrole"])
async def removerole(ctx, *, rmvrole: str):
    # role = ctx.message.content[len(str(config["prefix"]))+8:]
    alreadyhaveroles = []
    validrole = False
    toprole = 0
    # rolee = discord.utils.get(member.server.roles,name=addrole)
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
            await bot.remove_roles(ctx.message.author, discord.utils.get(ctx.message.server.roles, name=rmvrole))
            await bot.add_reaction(ctx.message, emoji='\N{WHITE HEAVY CHECK MARK}')
    else:
        pass
        await bot.add_reaction(ctx.message, emoji='\N{CROSS MARK}')


@bot.command(pass_context=True)
async def checkmember(ctx):
    if is_admin(ctx):
        notverified = []
        for member in ctx.message.server.members:
            is_verified = False
            for role in member.roles:
                if role.name == "Member":
                    is_verified = True
                    break
            if not is_verified:
                # await bot.add_roles(member, discord.utils.get(ctx.message.server.roles,name="Member"))
                notverified.append(str(member))
                # await bot.say("Added Member role to "+member.name)
        await bot.say(str(notverified) + " do not have the Member role")


@bot.command(pass_context=True)
async def test22(ctx):
    if is_admin(ctx):
        pass
        await bot.say(ctx.message.server.me.status)
        # bot.say(ctx.message.server.me.status)


@bot.command(pass_context=True)
async def test33(ctx):
    if is_admin(ctx):
        lt = bot.get_all_emojis()
        for em in lt:
            await bot.say(em.name)


@bot.command(pass_context=True)
async def roll(ctx, maximumroll: int):
    if len(ctx.message.content) == len(config["prefix"] + 4):
        await bot.say(ctx.message.author.name + " rolled a " + str(randint(1, 6)))
    else:
        await bot.say(ctx.message.author.name + " rolled a " + str(randint(1, maximumroll)))


@bot.command(pass_context=True)
async def purge(ctx, number: int):
    if is_admin(ctx):
        await bot.purge_from(ctx.message.channel, limit=number + 1)
        # await bot.send_message(ctx.message.channel, 'Deleted {} message(s)'.format(len(deleted)))


@bot.command(pass_context=True)
async def membercount(ctx):
    await bot.say("This server has {} users connected.".format(ctx.message.server.member_count))


@bot.command()
async def ping():
    await bot.say(":ping_pong: Pong!")


@bot.command()
async def randomcolor():
    randycolor = discord.Color(randint(0x000000, 0xFFFFFF))
    embed = discord.Embed(color=randycolor, description=str(randycolor))
    await bot.say("Color: " + str(randycolor))
    await bot.say(embed=embed)


@bot.command(pass_context=True, aliases=["newrole"])
async def createrole(ctx, *, rolename: str):
    if is_admin(ctx):
        currentroles = []
        for role in ctx.message.server.roles:
            currentroles.append(role.name.lower())
        if rolename.lower() not in currentroles:
            await bot.create_role(ctx.message.server, name=rolename, mentionable=True, hoist=False, reason="New Game Role")
            await bot.add_reaction(ctx.message, emoji=checkmarkemoji)
        else:
            await bot.add_reaction(ctx.message, emoji=xredemoji)
    else:
        await bot.add_reaction(ctx.message, emoji=xredemoji)


@bot.command(pass_context=True)
async def deleterole(ctx, *, rolename: str):
    if is_admin(ctx):
        currentroles = []
        toprole = 0
        validrole = False
        for role in ctx.message.server.roles:
            currentroles.append(role.name.lower())
            if role.name == 'overwatch':
                toprole = role.position
        for role in ctx.message.server.roles:
            if role.name == rolename and role.position <= toprole:
                validrole = True
        if rolename.lower() in currentroles and validrole:
            await bot.delete_role(ctx.message.server, discord.utils.get(ctx.message.server.roles, name=rolename))
            await bot.add_reaction(ctx.message, emoji=checkmarkemoji)
        else:
            await bot.add_reaction(ctx.message, emoji=xredemoji)
    else:
        await bot.add_reaction(ctx.message, emoji=xredemoji)


@bot.listen()
async def on_member_join(member):
    """is_verified = False
    for role in member.roles:
        if role.name == "Member":
            is_verified = True
            break
    if is_verified == False:"""
    await bot.send_message(discord.Object(id='382699994639237120'), str(member) + " has joined the server")
    # await bot.send_message(discord.Object(id='382699994639237120'),str(discord.utils.get(member.server.roles,name="Member")))
    # await bot.send_message(discord.Object(id='382699994639237120'),discord.utils.get(member.server.roles,name="Member"))
    # await bot.send_message(discord.Object(id='382699994639237120'),type(discord.utils.get(member.server.roles,name="Member")))
    await bot.add_roles(member, discord.utils.get(member.server.roles, name="Member"))


bot.run(config["tokens"]["discord"], bot=True, reconnect=True)
